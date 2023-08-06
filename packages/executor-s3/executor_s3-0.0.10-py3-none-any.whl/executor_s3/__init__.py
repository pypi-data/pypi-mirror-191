from executor_s3._impl import S3Resource, tar, upload, parquet, new_prefix  # noqa: F401
from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution("executor-s3").version
except DistributionNotFound:
    __version__ = 'local'
del get_distribution, DistributionNotFound
