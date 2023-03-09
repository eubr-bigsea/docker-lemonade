import mpld3
from flask import Flask, request, render_template
from matplotlib import pyplot as plt

from mpld3_ex1 import give_me_json
import request_lemonade as rl
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1> Hello world! </h1>"


@app.route('/models')
def models():
    model_id = request.args.get('id', default=None, type=int)
    return rl.get_models_limonero(model_id)


@app.route('/datasources')
def datasources():
    data_id = request.args.get('id', default=None, type=int)
    return rl.get_datasources_limonero(data_id)


@app.route('/xai/<id>')
def xai(id):
    model = rl.get_models_limonero(id)
    url_dataset = model['url']
    workflow_id = model['workflow_id']
    resp_tahiti =rl.get_workflows_tahiti(workflow_id)

    for task in resp_tahiti['tasks']:
        if 'data_source' in task['forms']:
            id_ds = task['forms']['data_source']['value']
            break
    dataset_name = rl.get_datasources_limonero(id_ds)

    return {
    "model": model['name'],
    "workflow": model['workflow_id'],
    "dataset": dataset_name['name'],
    "dataset_url": dataset_name['url']
    }


@app.route('/xai/mpld3/ex1')
def ex1_mpld3():
    give_me_json()
    return render_template('hi.html')


@app.route('/xai/mpld3/ex2')
def ex2_mpld3():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('Sine Wave')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    mpld3.save_html(fig, 'templates/hello.html')

    return render_template('hello.html')


@app.route('/xai/d3/ex1')
def ex1_d3():
    data = [4, 8, 15, 16, 23, 42]
    return render_template('d3js.html', data=data)


@app.route('/xai/d3/ex2')
def ex2_d3():
    data = [1.1, 2.2, 4.46, 2.12, 1.36, 5.002445, 4.1242]
    return render_template('d3_ex1.html', data=data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
