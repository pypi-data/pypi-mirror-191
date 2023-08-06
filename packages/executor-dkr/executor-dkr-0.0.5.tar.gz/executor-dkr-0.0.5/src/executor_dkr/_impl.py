import daggerml as dml
from executor_dkr._config import DAG_NAME, DAG_VERSION, TAG, CLUSTER_DAG, CLUSTER_VERSION
from executor_s3._impl import BUCKET, _upload_file
import json
import logging
import os
from subprocess import PIPE, Popen
import sys
from tempfile import NamedTemporaryFile


logger = logging.getLogger(__name__)


class DockerResource(dml.Resource):
    def __init__(self, resource_id, executor, tag=TAG):
        super().__init__(resource_id, executor, tag)

    @property
    def _json(self):
        return json.loads(self.id)

    @property
    def uri(self):
        return self._json['uri']

dml.register_tag(TAG, DockerResource)


def build(dag, resource, **kw):
    """build a docker image

    Parameters
    ----------
    dag : daggerml.Dag
        the dag that this image will be built for
    resource : executor_s3.S3Resource
        a tarball stored on s3 with a Dockerfile at its root.
    *kw : dict[str, nodeable]
        passed to func as metadata

    Returns
    -------
    DockerResource
        the docker image
    """
    fn = dag.load(DAG_NAME, DAG_VERSION)
    return fn(resource, **kw)


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


def _build_local(build_path, img_name, bucket=BUCKET):
    if os.path.exists(build_path):
        logger.info('building image...')
        build_path = os.path.abspath(build_path)
        with Popen(['docker', 'build', '-t', img_name, build_path], stdout=sys.stdout, stderr=sys.stderr) as proc:
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError('failed to build docker image: %s' % build_path)
    else:
        logger.info('not building image...')
    logger.info('getting image digest...')
    build_path = os.path.abspath(build_path)
    with Popen(['docker', 'inspect', "--format='{{index .Id}}'", img_name, build_path],
               stdout=PIPE) as proc:
        proc.wait()
        img_id = proc.stdout.read().decode().strip()
        if proc.returncode != 0:
            raise RuntimeError('failed to build docker image: %s' % build_path)
    key = f'executor/docker/data/local/{img_id}.tar'
    uri = f's3://{bucket}/{key}'
    with NamedTemporaryFile('w+', suffix='.tar') as f:
        with Popen(['docker', 'save', "-o", f.name, img_name]) as proc:
            proc.wait()
            if proc.returncode != 0:
                raise RuntimeError('failed to save docker image: %s' % img_name)
        if _upload_file(f.name, bucket, key):
            logger.info('uploaded image to %s...', uri)
        else:
            logger.info('using cached image from %s...', uri)
    _id = json.dumps({'uri': uri, 'name': img_name, 'id': img_id},
                     sort_keys=True, separators=(',', ':'))
    return _id
