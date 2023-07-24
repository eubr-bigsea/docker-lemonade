from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from explainable_ai.interpretability import TreeInterpretation, EnsembleInterpretation
from flask_restx import Resource, reqparse
from logger import setup_logger
import pickle

from xai_resource.load_resource import XaiLoadResource

logger = setup_logger()

tree_parser = reqparse.RequestParser()
tree_parser.add_argument('model_path', type=str, required=True, help='Model path is required.')
tree_parser.add_argument('data_path', type=str, required=True, help='Data path is required.')
tree_parser.add_argument('info_args', type=dict, required=True, help='info_args is required.')


class TreeApi(Resource):

    def delete(self):
        return "Delete data"

    def get(self):
        # Handle GET request logic for getting the model
        return 'Model Data'

    def post(self):
        args = tree_parser.parse_args()

        model_path = args['model_path']
        data_path = args['data_path']
        info_args = args['info_args']

        xai_lr = XaiLoadResource(
            data_is_local=data_path.split(":")[0] == "file",
            model_is_local=model_path.split(":")[0] == "file"
        )

        load_me = xai_lr.get_model(model_path.split("/")[-1])
        model = pickle.loads(load_me)
        df = xai_lr.get_data(data_path.split("/")[-1])

        tree_uai = TreeInterpretation(info_args, model, df)
        tree_uai.generate_arguments()

        logger.debug(info_args)

        return tree_uai.generated_args_dict


class EnsembleApi(Resource):

    def delete(self):
        return "Delete data"

    def get(self):
        # Handle GET request logic for getting the model
        return 'Model Data'

    def post(self):
        args = tree_parser.parse_args()

        model_path = args['model_path']
        data_path = args['data_path']
        info_args = args['info_args']

        xai_lr = XaiLoadResource(
            data_is_local=data_path.split(":")[0] == "file",
            model_is_local=model_path.split(":")[0] == "file"
        )

        load_me = xai_lr.get_model(model_path.split("/")[-1])
        model = pickle.loads(load_me)
        df = xai_lr.get_data(data_path.split("/")[-1])

        ensemble_uai = EnsembleInterpretation(info_args, model, df)
        ensemble_uai.generate_arguments()

        logger.debug(info_args)

        return ensemble_uai.generated_args_dict