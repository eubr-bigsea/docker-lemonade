from textwrap import dedent

from juicer.operation import Operation


class EnsembleOperation(Operation):

    FEATURE_IMPORTANCE = "feature importance"
    FOREST_IMPORTANCE = "forest importance"

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.model_data = named_inputs.get("ensemble_in")
        self.feature_importance = parameters.get(self.FEATURE_IMPORTANCE)
        self.forest_importance = parameters.get(self.FOREST_IMPORTANCE)
        self.task_id = self.parameters.get('task').get('id')
        self.operation_id = self.parameters.get('task').get('operation').get('id')

    def generate_code(self):
        code = dedent("""
            from juicer.explainable_ai.interpretability import EnsembleInterpretation
            from juicer.explainable_ai.plot_generate_xai import PltGenerate
            model_data = {mod_data}
            model = model_data[0]
            data = model_data[1]
            info_args = dict()                        
            ftr_imp = {feature_imporatnce}
            forest_imp = {forest_imporatnce}
            
            if ftr_imp:
                info_args['feature_importance'] = {{'n_feature': 3}}
            if forest_imp:
                info_args['forest_importance'] = {{'n_feature': 3}}
            
            uai = EnsembleInterpretation(info_args, model, data)
            uai.generate_arguments()
            plt_xai = PltGenerate(uai.generated_args_dict)
            fig = plt_xai.create_plots()
            
            emit_event('update task', status='COMPLETED',
            identifier='{task_id}',
            message=fig,
            type='IMAGE', title='{title}',
            task={{'id': '{task_id}'}},
            operation={{'id': {operation_id}}},
            operation_id={operation_id})
            
        """.format(
            mod_data=self.model_data,
            feature_imporatnce=self.feature_importance,
            forest_imporatnce=self.forest_importance,
            task_id=self.task_id,
            operation_id=self.operation_id,
            title="XAI"
        ))
        return code


class RegressionOperation(Operation):

    FEATURE_IMPORTANCE = "feature importance"
    P_VALUE = "p_value"

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.model_data = named_inputs.get("regression_in")
        self.feature_importance = parameters.get(self.FEATURE_IMPORTANCE)
        self.p_value = parameters.get(self.P_VALUE)
        self.task_id = self.parameters.get('task').get('id')
        self.operation_id = self.parameters.get('task').get('operation').get('id')

    def generate_code(self):
        code = dedent("""
            from juicer.explainable_ai.interpretability import LinearRegressionInterpretation
            from juicer.explainable_ai.plot_generate_xai import PltGenerate
            model_data = {mod_data}
            model = model_data[0]
            data = model_data[1]
            info_args = dict()                        
            ftr_imp = {feature_imporatnce}
            p_value = {p_value}

            if ftr_imp:
                info_args['feature_importance'] = {{'n_feature': 3}}
            if p_value:
                info_args['p_value'] = {{'intercept': [1]}}

            uai = LinearRegressionInterpretation(info_args, model, data)
            uai.generate_arguments()
            plt_xai = PltGenerate(uai.generated_args_dict)
            fig = plt_xai.create_plots()

            emit_event('update task', status='COMPLETED',
            identifier='{task_id}',
            message=fig,
            type='IMAGE', title='{title}',
            task={{'id': '{task_id}'}},
            operation={{'id': {operation_id}}},
            operation_id={operation_id})

        """.format(
            mod_data=self.model_data,
            feature_imporatnce=self.feature_importance,
            p_value=self.p_value,
            task_id=self.task_id,
            operation_id=self.operation_id,
            title="XAI"
        ))
        return code


class TreeOperation(Operation):

    FEATURE_IMPORTANCE = "feature importance"
    TREE_SURFACE = "tree surface"

    def __init__(self, parameters, named_inputs, named_outputs):
        Operation.__init__(self, parameters, named_inputs, named_outputs)

        self.model_data = named_inputs.get("tree_in")
        self.feature_importance = parameters.get(self.FEATURE_IMPORTANCE)
        self.tree_surface = parameters.get(self.TREE_SURFACE)
        self.task_id = self.parameters.get('task').get('id')
        self.operation_id = self.parameters.get('task').get('operation').get('id')

    def generate_code(self):
        code = dedent("""
            from juicer.explainable_ai.interpretability import TreeInterpretation
            from juicer.explainable_ai.plot_generate_xai import PltGenerate
            import requests
            model_data = {mod_data}
            model = model_data[0]
            data = model_data[1]
            info_args = dict()                        
            ftr_imp = {feature_importance}
            tree_surface = {tree_surface}

            if ftr_imp:
                info_args['feature_importance'] = {{'n_feature': 3}}
            if tree_surface:
                info_args['dt_surface'] = {{'max_deep': 4}}

            uai = TreeInterpretation(info_args, model, data)
            uai.generate_arguments()
            plt_xai = PltGenerate(uai.generated_args_dict)
            fig = plt_xai.create_plots()

            emit_event('update task', status='COMPLETED',
            identifier='{task_id}',
            message=fig,
            type='IMAGE', title='{title}',
            task={{'id': '{task_id}'}},
            operation={{'id': {operation_id}}},
            operation_id={operation_id})
            
            
            url = "http://172.17.0.1:5000/xai/resources"
            path1 = model_data[2]
            path2 = model_data[3]
            payload = {{'data': path1, 'model': path2}}
            response = requests.post(url, data=payload)

        """.format(
            mod_data=self.model_data,
            feature_importance=self.feature_importance,
            tree_surface=self.tree_surface,
            task_id=self.task_id,
            operation_id=self.operation_id,
            title="XAI"
        ))
        return code