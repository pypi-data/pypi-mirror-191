import os
import pandas as pd
# from concurrent.futures import ThreadPoolExecutor, as_completed
import daggerml as dml
import executor_s3 as s3
import executor_dkr as dkr
from executor_dkr._impl import run_shell
import json
import unittest
# from util import DmlTestBase

__here__ = os.path.dirname(__file__)
bucket = os.getenv('DML_BUCKET')

class DmlTestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._class_dags = []

    @classmethod
    def tearDownClass(cls):
        for dag in cls._class_dags:
            try:
                dag.fail()
            except dml.ApiError:
                pass
            dag.delete()

    def setUp(self):
        self._dags = []

    def tearDown(self):
        for dag in self._dags:
            try:
                dag.fail()
            except dml.ApiError:
                pass
            dag.delete()

    def new_dag(self, name=None, version=None, keep=False):
        if name is None:
            name = self.id()
        dag = dml.Dag.new(name, version)
        if dag is not None:
            if keep:
                self._class_dags.append(dag)
            else:
                self._dags.append(dag)
        return dag

class TestK8s(DmlTestBase):

    def test_new_tar(self):
        assert bucket is not None
        dag = self.new_dag(self.id(), keep=True)
        path = os.path.join(__here__, 'container/')
        resp = run_shell('dml-dkr', 'build', '-d', path, '--bucket', bucket, '-v', f'bucket={bucket}')
        resp = json.loads(resp)
        build_res = dag.load(resp['dag_name'], resp['dag_version'])
        resp = dkr.run(dag, build_res['image'], 5, 7, 12)
        assert isinstance(resp.to_py(), s3.S3Resource)
        df = pd.read_parquet(resp.to_py().uri)
        assert df.shape == (5, 7)
        dag.commit(None)

    # def test_parallel_execution(self):
    #     dag = self.new_dag()
    #     path = os.path.join(__here__, 'container/')
    #     tar_resource = s3.tar(dag, path)
    #     img = dkr.build(dag, tar_resource)
    #     with ThreadPoolExecutor(max_workers=25) as pool:
    #         futs = {pool.submit(dkr.run, dag, img, n, 7, 12): n for n in range(2, 200)}
    #         for fut in as_completed(futs):
    #             n = futs[fut]
    #             data = fut.result()
    #             assert isinstance(data, dml.Node)
    #             df = pd.read_parquet(data.to_py().uri)
    #             assert list(df.shape) == [n, 7]
