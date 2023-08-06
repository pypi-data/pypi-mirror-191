import os
import json
import boto3
import base64
import tarfile
import logging
import daggerml as dml
from uuid import uuid4
from hashlib import md5
from tempfile import NamedTemporaryFile
from botocore.exceptions import ClientError
from subprocess import PIPE, run as run_shell
from pkg_resources import get_distribution, DistributionNotFound
from executor_s3._config import TAG, DAG_NAME, DAG_VERSION, BUCKET
try:
    __version__ = get_distribution("executor-s3").version
except DistributionNotFound:
    __version__ = 'local'


logger = logging.getLogger(__name__)
this_dir = os.path.dirname(os.path.realpath(__file__))


class S3Resource(dml.Resource):
    def __init__(self, resource_id, executor, tag=TAG):
        super().__init__(resource_id, executor, tag)

    @property
    def _json(self):
        return json.loads(base64.decodebytes(self.id.encode()).decode())

    @property
    def uri(self):
        return self._json['uri']

    @property
    def type(self):
        return self._json['type']

dml.register_tag(TAG, S3Resource)


def _md5sum(path):
    hash_md5 = md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def _run_s3_dag(s3_dag, node_id, type_):
    dag = dml.Dag.from_claim(s3_dag.executor, s3_dag.secret, 1, node_id)
    if dag is None:
        raise RuntimeError('Failed to claim node!')
        return
    with dag:
        expr = dag.expr.to_py()
        assert len(expr) == 3 and expr[1] == 'upload', 'malformed expression'
        assert isinstance(expr[2], str), 'malformed expression'
        assert expr[2].startswith('s3://'), f'{type_} s3 loc: {expr[2]} doesnt start with s3!'
        _id = json.dumps({'uri': expr[2], 'type': str(type_)},
                         sort_keys=True, separators=(',', ':'))
        _id = base64.encodebytes(_id.encode()).decode().replace('\n', '')
        dag.commit(S3Resource(_id, s3_dag.executor))
    return


def _exec_remote(dag, uri, type_):
    resp = dag.load(DAG_NAME, DAG_VERSION)
    s3_dag, fn = dml.Dag(**resp[0].to_py()), resp[1]
    resp = fn.call_async(uri)
    if resp.check() is None:
        _run_s3_dag(s3_dag, resp.id, type_)
    return resp.wait(2)


def s3_obj_exists(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


def _upload_file(path, bucket, key):
    s3client = boto3.client('s3')
    if not s3_obj_exists(s3client, bucket, key):
        s3client.upload_file(path, bucket, key)
        return True
    return False


def upload_tar(dag, path, bucket=BUCKET):
    path = os.path.abspath(path)
    proc = run_shell([f'{this_dir}/hash-tar.sh', path], stdout=PIPE, stderr=PIPE)
    if proc.returncode != 0:
        raise RuntimeError('failed to get hash of file: %s', path)
    md5 = proc.stdout
    assert md5 is not None, 'bad md5sum'
    key = f'executor/s3/data/tar/{md5.decode()}.tar'
    if _upload_file(path, bucket, key):
        logger.info('uploaded tarball %r to s3://%s/%s', path, bucket, key)
    else:
        logger.info('%r using cached value s3://%s/%s', path, bucket, key)
    return _exec_remote(dag, f's3://{bucket}/{key}', 'tarball')


def tar(dag, path, bucket=BUCKET):
    path = os.path.abspath(path)
    logger.info('set path to: %r', path)
    with NamedTemporaryFile('w+') as f:
        with tarfile.open(f.name, "w:gz") as tar:
            tar.add(path, arcname='/')
        f.seek(0)
        return upload_tar(dag, f.name, bucket=bucket)


def upload(dag, path, bucket=BUCKET):
    path = os.path.abspath(path)
    logger.info('set path to: %r', path)
    md5_hash = _md5sum(path)
    key = f'executor/s3/data/misc/{md5_hash}/' + path.split('/')[-1]
    if _upload_file(path, bucket, key):
        logger.info('uploaded file %r to s3://%s/%s', path, bucket, key)
    else:
        logger.info('%r using cached value s3://%s/%s', path, bucket, key)
    return _exec_remote(dag, f's3://{bucket}/{key}', 'misc')


def parquet(dag, df, bucket=BUCKET):
    import pandas as pd
    import pandas.util as pu
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df must be a dataframe')
    _hash = pu.hash_pandas_object(df).sum()
    key = f'executor/s3/data/dataframe-pandas/{_hash}.parquet'
    s3_loc = f's3://{bucket}/{key}'
    df.to_parquet(s3_loc)
    return _exec_remote(dag, s3_loc, 'parquet')


def new_prefix(dag, bucket=BUCKET):
    return _exec_remote(dag, f's3://{bucket}/executor/s3/data/unique-prefix/{uuid4().hex}/', 'prefix')
