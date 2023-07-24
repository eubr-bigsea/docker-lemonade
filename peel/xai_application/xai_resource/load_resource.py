from logger import setup_logger
import pandas as pd
import pickle
from pyarrow import fs

logger = setup_logger()

class XaiLoadResource:

    def __init__(self, data_is_local=False, model_is_local=False):
        self.data_is_local = data_is_local
        self.model_is_local = model_is_local

    def get_model(self, model_name):
        if self.model_is_local:
            model_path = '/models/' + model_name
            arrow = fs.LocalFileSystem()
            exists = arrow.get_file_info(model_path).is_file
            if not exists:
                logger.error(f'class {self.__class__.__name__} tried load model {model_name}, '
                             f'but this model doesnt exist!!')
                raise ValueError(f'class {self.__class__.__name__} tried load model {model_name}, '
                                 f'but this model doesnt exist!!')
            with arrow.open_input_stream(model_path) as stream:
                rd = stream.readall()
            return rd

    def get_data(self, data_name):
        if self.data_is_local:
            if data_name.endswith(".csv"):
                data_path = '/data/' + data_name
                df = pd.read_csv(data_path, index_col=False)
                return df
        else:
            logger.error(f"class {self.__class__.__name__} doesnt know how to load {data_name}")
            raise NotImplementedError(f"class {self.__class__.__name__} doesnt know how to load {data_name}")

