import collections
import logging
import pandas as pd
import time
import requests
from airflow.operators.python import PythonOperator
from datetime import datetime
import json
import awswrangler as wr

DIEGO_MAX_ROWS = 10000000
log = logging.getLogger(__name__)


class DiegoOperator(PythonOperator):
    def __init__(self, task_id, cube_id, platform_url: str, python_callable, op_kwargs=None, ignore_empty_dataframe=False, sleep_between_chunks=30,
                 diego_chunksize=DIEGO_MAX_ROWS, date_columns: list = None, pandas_kwargs: dict = None, retries=2,full_load=False, **kwargs) -> None:
        """
        Operator that expects a python_callable that returns or yields a pandas Dataframe to process and insert the corresponding Dataframe into a csv to Diego

        :param task_id: id of the this task
        :param retries: number of times to retry this task in case of failure
        :param cube_id: id of the cube to be stored the data
        :param platform_url: id of the platform to be stored the data
        :param python_callable: it is expected a Callable that returns a pandas DataFrame or else a TypeError will be raised
        :param op_kwargs: python_callable kwargs
        :param ignore_empty_dataframe: will consider a empty dataframe returned from python_callable as a success
        :param sleep_between_chunks: number in seconds to wait before sending another chunk of dataframe to Diego
        :param diego_chunksize: max number of rows per chunk to send to Diego
        :param date_columns: list of columns containing the name of the columns that are date type to be pre-processed (SID have specific requirements for date types)
        :param full_load: wheter or not the destiny cube will have its data erased before inserting new data. Values True or False (default)
        :param pandas_kwargs: dictionary containing the parameters to be forwarded to pandas 'to_parquet' method
        :param kwargs: all kwargs will be forwarded to the PythonOperator as parameters
        """
        if op_kwargs is None:
            op_kwargs = dict()
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        if date_columns is None:
            date_columns = list()

        super().__init__(task_id=task_id, python_callable=python_callable, op_kwargs=op_kwargs, retries=retries, **kwargs)
        self.cube_id = cube_id
        self.platform_url = platform_url
        self.ignore_empty_dataframe = ignore_empty_dataframe
        self.pandas_kwargs = pandas_kwargs
        self.sleep_between_chunks = sleep_between_chunks
        self.date_columns = date_columns
        self.diego_chunksize = diego_chunksize
        self.task_id = task_id
        self.full_load = full_load

    def send_file_path_to_diego(self, file_path):
        data_format = json.dumps({
            "destinationId": self.cube_id,
            "file": file_path,
            "pattern": ".*.parquet",
            "fullLoad": self.full_load
            })

        endpoint = f"{self.platform_url}/controller/dataloader/cube-load/s3"
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            endpoint,
            data=data_format,
            headers=headers
        )

        print(f"File sent to Diego to path {file_path}")
        print(f"Diego response {response.text}")

        return response

    def __upload_df_to_s3_temp(self, df: pd.DataFrame, path, part_number, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        wr.s3.to_parquet(
            df=df,
            path=f"{path}/{part_number}.parquet"
)

        return True


    def __upload_pandas_df_to_diego(self, df, path, part_number, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        rows = df.shape[0]

        if rows <= self.diego_chunksize:
            self.__upload_df_to_s3_temp(df=df, path=path, part_number=part_number, pandas_kwargs=pandas_kwargs)
        else:
            list_df = [df[i:i + self.diego_chunksize] for i in range(0, df.shape[0], self.diego_chunksize)]
            for i, df_element in enumerate(list_df):
                self.__upload_df_to_s3_temp(df=df_element, path=path, part_number=part_number, pandas_kwargs=pandas_kwargs)
                time.sleep(self.sleep_between_chunks)

    def upload_df_to_diego(self, df, path, part_number, pandas_kwargs=None):
        if pandas_kwargs is None:
            pandas_kwargs = dict()
        if isinstance(df, pd.DataFrame):
            return self.__upload_pandas_df_to_diego(df=df, path=path, part_number=part_number, pandas_kwargs=pandas_kwargs)
        else:
            raise TypeError(f'df must be a pandas DataFrame object, it is type: {type(df)}')

    def __execute_df(self, df, part_number, path):
        if not isinstance(df, pd.DataFrame):
            raise TypeError(f'The callable must return a pandas DataFrame object, it returned: {type(df)}')

        if self.ignore_empty_dataframe and df.shape[0] == 0:
            return []
        elif not self.ignore_empty_dataframe and df.shape[0] == 0:
            raise ValueError(f'The dataframe passed is empty {df.shape}, please use a valid dataframe')

        return self.upload_df_to_diego(df, path=path, part_number=part_number, pandas_kwargs=self.pandas_kwargs)


    def execute(self, context):
        df = super().execute(context)

        temp_file_path = f"cortex-data-lakehouse-metastore-development/temp-files-diego/{self.task_id}/{self.cube_id}/{str(hash(datetime.utcnow().isoformat()))}"

        if isinstance(df, collections.Iterator):
            for part_number, df_part in enumerate(df):
                self.__execute_df(df=df_part, part_number=part_number, path=f"s3://{temp_file_path}")
        else:
            self.__execute_df(df=df, part_number=1, path=f"s3://{temp_file_path}")

        response = self.send_file_path_to_diego(temp_file_path)

        if not self.ignore_empty_dataframe and not response.json().get("replyId"):
            raise ValueError('There were no dataframes written to Diego. Please check if your dataframes are empty')

        context['task_instance'].xcom_push(key='platform_url', value=self.platform_url)
        context['task_instance'].xcom_push(key='execution_ids', value=[response.json().get("replyId") if response.json().get("replyId") else None])
