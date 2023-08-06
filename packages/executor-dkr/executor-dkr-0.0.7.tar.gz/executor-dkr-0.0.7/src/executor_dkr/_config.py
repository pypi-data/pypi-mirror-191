import daggerml as dml
import logging
import os

logger = logging.getLogger(__name__)

DAG_NAME = TAG = 'com.daggerml.resource.docker'
DAG_VERSION = 1

CLUSTER_DAG = 'com.daggerml.resource.cluster'
CLUSTER_VERSION = 1

BUCKET = os.getenv('DML_BUCKET')

def init():
    dag = dml.Dag.new(DAG_NAME, DAG_VERSION)
    if dag is not None:
        logger.info('committing dag %r now', dag)
        dag.commit([dag.executor, dag.secret])
    return
