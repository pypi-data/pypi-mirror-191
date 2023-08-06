from airflow.models import BaseOperator
from data_product_sdk.aws.glue_databrew import AwsGlueDatabrew


class DatabrewProfilerOperator(BaseOperator):
    def __init__(*, self, task_id, job_name, retries=1, **kwargs) -> None:
        self.job_name = job_name
        super().__init__(task_id=task_id, retries=retries, **kwargs)

    def execute(self, context) -> None:
        glue_databrew = AwsGlueDatabrew()
        glue_databrew.start_job_run(job_name=self.job_name)
