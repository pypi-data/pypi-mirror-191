import daggerml as dml
import os


TAG = 'com.daggerml.resource.s3'
DAG_NAME = TAG
DAG_VERSION = 1
BUCKET = os.getenv('DML_BUCKET')

DAG = dml.Dag.new(DAG_NAME, DAG_VERSION)
if DAG is not None:
    DAG.commit([vars(DAG), [DAG.executor, 'upload']])
