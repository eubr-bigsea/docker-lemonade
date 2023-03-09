from unittest import TestCase

from model_to_understand import ModelUAI
from request_lemonade import get_models_limonero


class TestModelUAI(TestCase):

    def test_model_uai(self):
        model = get_models_limonero(42)
        print(model)
        model_uai = ModelUAI(**model)

        for k, v in model.items():
            self.assertEqual(model_uai.__dict__[k], v)






