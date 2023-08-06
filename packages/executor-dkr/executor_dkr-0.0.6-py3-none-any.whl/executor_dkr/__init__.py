from pkg_resources import get_distribution, DistributionNotFound
from executor_dkr._impl import DockerResource, run  # noqa: F401
try:
    __version__ = get_distribution("executor-dkr").version
except DistributionNotFound:
    __version__ = 'local'
del get_distribution, DistributionNotFound
