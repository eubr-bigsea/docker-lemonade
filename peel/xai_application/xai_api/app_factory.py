import os
from flask import Flask
from flask_restx import Api
from xai_api.interpretability_api import TreeApi, EnsembleApi


def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'


    api = Api(app, prefix="/xai")

    map_routes = {
        TreeApi: '/tree',
        EnsembleApi: '/ensemble'
    }

    for class_name, route in map_routes.items():
        api.add_resource(class_name, route)

    return app