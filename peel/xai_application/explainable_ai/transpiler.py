import os

from juicer.transpiler import Transpiler
import juicer.explainable_ai.model_xai_operation as md_xai_op
import juicer.explainable_ai.interpretation_operation as inter_op


class ExplainableAITranspiler(Transpiler):

    def __init__(self, configuration, slug_to_op_id=None, port_id_to_port=None):
        super(ExplainableAITranspiler, self).__init__(configuration, os.path.abspath(os.path.dirname(__file__)),
                                                   slug_to_op_id, port_id_to_port)
        self._assign_operations()

    def _assign_operations(self):

        model_xai = {
            "load-model": md_xai_op.ModelXAIOperation
        }

        int_op = {
            "tree_ensemble": inter_op.EnsembleOperation,
            "regression": inter_op.RegressionOperation,
            "tree": inter_op.TreeOperation
        }

        self.operations = {}

        for ops in [model_xai, int_op]:
            self.operations.update(ops)
