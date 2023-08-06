import json
from http import HTTPStatus

import requests
import logging

from airflow.models import Variable
from airflow.sensors.base import BaseSensorOperator

from data_product_sdk.cortex_airflow.data_platform.operators.diego_operators import DiegoOperator


logger = logging.getLogger(__name__)


class DiegoSensor(BaseSensorOperator):
    def __init__(self, poke_interval=30, timeout=300, platform_url: str = None, diego_operator: DiegoOperator = None, retries=20, **kwargs) -> None:
        """
        Sensor that works in conjunction with :class:`SidOperator`. It is used to monitor if SID is done loading the data into the platform

        :param poke_interval: time in seconds between API calls to SID
        :param timeout: time in seconds of sensor timeout
        :param platform_url: id of the platform to be stored the data
        :param diego_operator: DiegoOperator object that was used to input data, its metadata will be utilized to monitor if the data was upload successfully
        :param kwargs: all kwargs will be forwarded to the BaseSensorOperator as parameters
        """
        super().__init__(poke_interval=poke_interval, timeout=timeout, retries=retries, **kwargs)
        self.diego_operator = diego_operator
        self.platform_url = platform_url
        self.completed_executions = dict()

    def check_completed_execution_id(self, platform_url, execution_id: str):
        url = f"{platform_url}/controller/dataloader/cube-load/s3/{execution_id}"
        headers = {'Content-Type': 'application/json'}

        response = requests.request("GET", url, headers=headers)

        if response.status_code != HTTPStatus.OK:
            raise ValueError(f'It was expected a {HTTPStatus.OK} http status code, it was received: {response.status_code} '
                            f'\n {response.text}')
        response_json = response.json()
        return response_json

    def __check_completed_execution_ids(self, execution_ids: list, platform_url: str):

        # self.completed_execution[execution_id] = response.json()['replyId']

        for execution_id in execution_ids:
            response = self.check_completed_execution_id(execution_id=execution_id, platform_url=platform_url)
            logger.info(f'EXECUTION RESPONSE: {response}')
            completed = response['completed'] and response.get('success', False)
            self.completed_executions[execution_id] = completed
        logging.info(f'EXECUTION_IDS_COMPLETION: {self.completed_executions}')


    def check_execution_ids_completed(self, execution_ids: list, platform_url: str):
        self.__check_completed_execution_ids(execution_ids=execution_ids, platform_url=platform_url)
        return all(self.completed_executions.values())

    def poke(self, context, execution_ids=None, platform_url=None, diego_operator=None) -> bool:
        platform_url = self.platform_url if platform_url is None else platform_url
        diego_operator = self.diego_operator if diego_operator is None else diego_operator
        assert (execution_ids and platform_url) or diego_operator, \
            'You need to pass a execution_id platform_url or a diego_operator as valid parameters'

        if execution_ids and platform_url:
            completed = self.check_execution_ids_completed(execution_ids=execution_ids, platform_url=platform_url)
            return completed
        elif diego_operator is not None:
            execution_ids = context['task_instance'].xcom_pull(task_ids=diego_operator.task_id, key='execution_ids')
            platform_url = context['task_instance'].xcom_pull(task_ids=diego_operator.task_id, key='platform_url')
            if diego_operator.ignore_empty_dataframe and not execution_ids and not platform_url:
                logging.info('ACCEPTING EMPTY DATAFRAME')
                return True

        logging.info(f'POKE:\n EXECUTION ID: {execution_ids}')
        completed = self.check_execution_ids_completed(execution_ids=execution_ids, platform_url=platform_url)

        return completed
