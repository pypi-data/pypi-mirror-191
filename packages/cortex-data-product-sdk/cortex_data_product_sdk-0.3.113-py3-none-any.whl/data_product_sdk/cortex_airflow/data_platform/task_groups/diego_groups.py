from airflow.utils.task_group import TaskGroup
from data_product_sdk.cortex_airflow.data_platform.operators.diego_operators import DiegoOperator, DIEGO_MAX_ROWS
from data_product_sdk.cortex_airflow.data_platform.sensors.diego_sensors import DiegoSensor
import logging

def create_diego_upload_flow(task_id, platform_url: str, cube_id: str, python_callable, op_kwargs=None, ignore_empty_dataframe=False,
                           sleep_between_chunks=30, diego_chunksize=DIEGO_MAX_ROWS, date_columns=None, pandas_kwargs=None, timeout=300, full_load=False):
    """
    Creates an upload flow using a :class:`DiegoOperator` and a :class:`DiegoSensor`

    :param task_id: id of the this task
    :param platform_url: id of the platform to be stored the data
    :param username: platform login username
    :param password: platform login password
    :param cube_id: id of the cube to be stored the data
    :param python_callable: it is expected a Callable that returns a pandas DataFrame or else a TypeError will be raised
    :param op_kwargs: python_callable kwargs
    :param ignore_empty_dataframe: will consider a empty dataframe returned from python_callable as a success
    :param sleep_between_chunks: number in seconds to wait before sending another chunk of dataframe to Diego
    :param diego_chunksize: max number of rows per chunk to send to diego
    :param date_columns: list of columns containing the name of the columns that are date type to be pre-processed (diego have specific requirements for date types)
    :param pandas_kwargs: dictionary containing the parameters to be forwarded to pandas 'to_csv' method
    :param full_load: if True the destiny cube will drop all data before insert new ones. If false, only new data will be inserted
    :return: TaskGroup with the upload flow
    """
    with TaskGroup(task_id) as diego_group:
        logging.info("Creating operator task")
        diego_operator = DiegoOperator(task_id=f'operator', cube_id=cube_id, platform_url=platform_url, python_callable=python_callable,
                                   op_kwargs=op_kwargs, ignore_empty_dataframe=ignore_empty_dataframe, sleep_between_chunks=sleep_between_chunks,
                                   diego_chunksize=diego_chunksize, date_columns=date_columns, pandas_kwargs=pandas_kwargs, full_load=full_load)

        logging.info("Creating sensor task")
        diego_sensor = DiegoSensor(task_id=f'sensor', platform_url=platform_url, diego_operator=diego_operator, timeout=timeout)

        logging.info("Executing operator and sensor sequentailly")
        diego_operator >> diego_sensor

    return diego_group
