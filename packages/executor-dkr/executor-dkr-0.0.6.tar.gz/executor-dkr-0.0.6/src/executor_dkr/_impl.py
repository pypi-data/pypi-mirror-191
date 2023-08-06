import base64
import boto3
from botocore.exceptions import ClientError
import daggerml as dml
from executor_dkr._config import (
    DAG_NAME, DAG_VERSION, TAG, CLUSTER_DAG, CLUSTER_VERSION
)
import json
import logging
import os
from subprocess import PIPE, Popen
import sys
from tempfile import NamedTemporaryFile
from uuid import uuid4
from warnings import warn

logger = logging.getLogger(__name__)

class DockerResource(dml.Resource):
    def __init__(self, resource_id, executor, tag=TAG):
        super().__init__(resource_id, executor, tag)

    @property
    def _json(self):
        return json.loads(base64.b64decode(self.id))

    @property
    def uri(self):
        return self._json['uri']

    @property
    def name(self):
        return self._json.get('name')

dml.register_tag(TAG, DockerResource)

def run(dag, image, *args, **kw):
    """run a docker image on kubernetes

    Parameters
    ----------
    dag : daggerml.Dag
        the dag that this image will be built for
    image : DockerResource
        the docker image you want to run
    *args : nodeable
        args passed to func
    *kw : dict[str, nodeable]
        passed to func as metadata

    Returns
    -------
    Node
        the result of running that image
    """
    cluster = dag.load(CLUSTER_DAG, CLUSTER_VERSION)
    return cluster(image, *args, **kw)


def s3_obj_exists(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


def _upload_file(path, bucket, key):
    s3client = boto3.client('s3')
    logger.debug('checking to see if object exists on s3...')
    if not s3_obj_exists(s3client, bucket, key):
        logger.debug('uploading file...')
        s3client.upload_file(path, bucket, key)
        return True
    logger.debug('using cached file version...')
    return False


def run_shell(*args, stdout=PIPE, stderr=sys.stderr):
    with Popen(args, stdout=stdout, stderr=stderr) as proc:
        proc.wait()
        if proc.returncode != 0:
            logger.error('failed to run args: %r', args)
            raise RuntimeError(json.dumps({
                'message': 'failed shell evocation',
                'command': args,
                'code': 400
            }))
        if stdout is PIPE:
            return proc.stdout.read().decode().strip()


def _build_local(build_path, img_name, bucket):
    if build_path is not None:
        logger.info('building image...')
        build_path = os.path.abspath(build_path)
        run_shell('docker', 'build', '-t', img_name, build_path, stdout=sys.stdout)
        # run_shell('bash', '-c', f'docker build -t {img_name} {build_path} 1>&2')
    else:
        logger.debug('not building image...')
    logger.debug('getting image digest...')
    img_id = run_shell('docker', 'inspect', "--format='{{index .Id}}'", img_name)
    img_id = img_id.replace("'", '')
    key = f'executor/docker/data/local/{img_id}.tar'
    uri = f's3://{bucket}/{key}'
    with NamedTemporaryFile('w+', suffix='.tar') as f:
        logger.info('saving image to %r', uri)
        run_shell('docker', 'save', '-o', f.name, img_name, stdout=sys.stdout)
        logger.debug('uploading image... this might take a while...')
        if _upload_file(f.name, bucket, key):
            logger.debug('uploaded image to %s...', uri)
        else:
            logger.debug('using cached image from %s...', uri)
    _id = json.dumps({'uri': uri, 'name': img_name, 'id': img_id},
                     sort_keys=True, separators=(',', ':'))
    logger.debug('returning with resource ID: %r', _id)
    return _id

def build(dag_name, build_path, img_name, bucket, **kw):
    try:
        with dml.Dag.new(dag_name) as dag:
            logger.debug('loading dag')
            ex, sec = dag.load(DAG_NAME, DAG_VERSION).to_py()
            build_resource = {'img_name': img_name}
            if build_path is not None:
                logger.debug('build path is not None')
                try:
                    import executor_s3 as s3
                    build_resource['tarball'] = s3.tar(dag, build_path, bucket=bucket).to_py()
                except ImportError:
                    warn('install executor-s3 for better docker-build tracking')
            if build_resource.get('tarball') is None:
                logger.debug('tarball was nil, so defining uuid')
                build_resource['uuid'] = str(uuid4())
            logger.info('build resource: %r', build_resource)
            fn = dag.from_py([ex, 'build'])
            logger.debug('calling function')
            node_waiter = fn.call_async(build_resource)
            node_waiter.check()
            if node_waiter.result is None:
                logger.debug('running build-local')
                with dml.Dag.from_claim(ex, sec, 600, node_waiter.id) as ex_dag:
                    _id = _build_local(build_path, img_name, bucket)
                    logger.debug('got resource ID: %r', _id)
                    _id = base64.b64encode(_id.encode()).decode()
                    logger.debug('base64 resource ID: %r', _id)
                    dkr_resource = DockerResource(_id, ex)
                    logger.debug('committing docker resource: %r', dkr_resource)
                    ex_dag.commit(dkr_resource)
                logger.debug('waiting for node')
                node_waiter.wait(2)
            else:
                logger.debug('using cached value')
            logger.debug('committing %r', node_waiter.result)
            res = node_waiter.result
            dag.commit({'build-resource': build_resource,
                        'image': res})
    except Exception:
        logger.exception('ruh roh!')
        raise
    return {
        'dag_name': dag.name,
        'dag_version': dag.version,
        'image-key': 'image',
        'meta-key': 'build-resource'
    }
