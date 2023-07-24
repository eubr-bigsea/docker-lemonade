import logging
import time
import os
from flask import Flask, Response, request
from celery import Celery

app = Flask(__name__)
simple_app = Celery('xai',
                    broker='amqp://admin:mypass@rabbit:5672',
                    backend='rpc://')

app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'

# Configure the Flask logger
app.logger.setLevel(logging.DEBUG)  # Set the desired log level
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add a StreamHandler to redirect logs to the console (Docker logs)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
app.logger.addHandler(stream_handler)

def generate_stream(task):
    count = 0
    while not task.ready():
        count += 1
        yield f'data: Processing iteration {count}\n\n'
        time.sleep(1)
    result = simple_app.AsyncResult(task.id).result
    yield f'data: {result}\n\n'

@app.route('/simple_start_task')
def call_method():
    app.logger.info("Invoking Method ")
    r = simple_app.send_task('xai_tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    app.logger.info(r.backend)
    return r.id


@app.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@app.route('/simple_task_result/<task_id>')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)

@app.route('/stream')
def stream():
    task = simple_app.send_task('xai_tasks.execute_method')
    return Response(generate_stream(task), mimetype='text/event-stream')


@app.route('/xai/resources', methods=['POST'])
def resource():
    path1 = request.form.get('data')
    path2 = request.form.get('model')
    #
    data_name = path1.split('/')[-1]
    data_path = '/app/data/'+data_name

    task = simple_app.send_task('xai_tasks.get_datasource', kwargs={'data_path': data_path})
    result = simple_app.AsyncResult(task.id).result

    app.logger.info(f"data: {result if result is not None else data_path}")
    app.logger.info(f"model: {path2}")

    return "Received URL arguments successfully!"
