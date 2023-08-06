from argparse import ArgumentDefaultsHelpFormatter
import daggerml._clink as clink
import executor_dkr as dkr
from executor_dkr._config import BUCKET, init
from executor_dkr._impl import build as _build
from getpass import getuser
import json
import logging
import logging.config

logging_config = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'executor_dkr': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

@clink.arg('--version', action='version', version=dkr.__version__)
@clink.cli(description="DaggerML's docker-build command line tool",
           formatter_class=ArgumentDefaultsHelpFormatter)
def cli(*args, **kwargs):
    raise Exception('no command specified')

@clink.arg('-d', '--build-dir',
           help='if specified, builds first and stores the tarball for posterity (if executor-s3 is installed)')
@clink.arg('--img-name', default='img', help='what name to give the image')
@clink.arg('--dag-name', default=getuser() + '/docker-build', help='what to name the dag')
@clink.arg('--bucket', default=BUCKET, help='s3 bucket')
@clink.arg('-v', '--verbose', action='store_true', dest='verbose', help='verbose?')
@cli.command(help='configure DaggerML API',
             formatter_class=ArgumentDefaultsHelpFormatter)
def build(dag_name, build_dir, img_name, bucket, verbose):
    log_level = 'DEBUG' if verbose else 'INFO'
    logging_config['loggers']['executor_dkr']['level'] = getattr(logging, log_level)
    logging_config['loggers']['executor_s3'] = logging_config['loggers']['executor_dkr']
    logging_config['loggers']['daggerml'] = logging_config['loggers']['executor_dkr']
    logging.config.dictConfig(logging_config)
    init()
    resp = _build(dag_name, build_dir, img_name, bucket)
    print(json.dumps(resp, sort_keys=True, separators=(',', ':')))
    return
