import time
from celery import Celery
from celery.utils.log import get_task_logger
import pandas as pd

logger = get_task_logger(__name__)

app = Celery('xai',
             broker='amqp://admin:mypass@rabbit:5672',
             backend='rpc://')


@app.task
def get_datasource(data_path):
    df = pd.read_csv(data_path)
    if isinstance(df, pd.DataFrame):
        return df.head().to_dict()
    else:
        return None


@app.task
def longtime_add(x, y):
    logger.info('Got Request - Starting work ')
    time.sleep(4)
    logger.info('Work Finished ')
    return x + y


@app.task
def execute_method():
    time.sleep(15)
    return "Long-running task completed."
