from lime import lime_tabular


from explainer.gpx import GPX
from lime import lime_tabular

from xai_application.explainable_ai.understand_ai import Understanding


class Explanation(Understanding):

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 mode=None):

        """

        :param arguments_used:
        :param model_to_understand:
        :param data_source:
        :param feature_names:
        :param target_name:
        """

        super().__init__(arguments_used, model_to_understand, data_source )
        self.mode = mode


class GeneticProgrammingExplainer(Explanation):

    def __init__(self, arguments_used, model_to_understand, data_source,
                 mode='classification', gp_solver='gplearn',  num_samples=500):
        super().__init__(arguments_used, model_to_understand, data_source, mode)
        self.num_samples = num_samples
        self.explainer = None
        self.gp_solver = gp_solver
        self.explainer = GPX(x=self.data_source[self.feature_names[:-1]],
                             y=self.data_source[self.feature_names[-1]],
                             model_predict=self.model_to_understand.predict,
                             gp_model=self.gp_solver,
                             noise_set_num_samples=self.num_samples,
                             diff_as_numpy=False)

    @property
    def gp_solver(self):
        return self._gp_solver

    @gp_solver.setter
    def gp_solver(self, gp_solver):
        if gp_solver == 'gplearn':
            from gplearn.genetic import SymbolicRegressor
            gp_hyper_parameters = {'population_size': 20,
                                   'generations': 50,
                                   'stopping_criteria': 0.00001,
                                   'p_crossover': 0.5,
                                   'p_subtree_mutation': 0.2,
                                   'p_hoist_mutation': 0.1,
                                   'p_point_mutation': 0.2,
                                   'const_range': (-5.0, 5.0),
                                   'parsimony_coefficient': 0.01,
                                   'init_depth': (2, 3),
                                   'n_jobs': -1,
                                   'low_memory': True,
                                   'function_set': ('add', 'sub', 'mul', 'div')}
            self._gp_solver = SymbolicRegressor(**gp_hyper_parameters)
        else:
            raise ValueError('Genetic Programming solver does not exist')

    def _uai_feature_importance(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None:
            self.explainer.instance_understanding(instance)
            names = []
            values = []

            for k, v in self.explainer.derivatives_generate(instance, as_numpy=False).items():
                names.append(k)
                values.append(v)

            return values, names

        else:

            raise ValueError(f"{self.__class__.__name__} must of a instance")


class LocalExplanation(Explanation):
    def __init__(self, arguments_used, model_to_understand,
                 data_source, mode='classification'):
        super().__init__(arguments_used, model_to_understand, data_source, mode)

        self.mode = mode
        x_lime = self.data_source[self.feature_names[:-1]].values
        self.explainer = lime_tabular.LimeTabularExplainer(training_data=x_lime,
                                                           mode=self.mode,
                                                           feature_names=self.feature_names)

    def _uai_generate_table(self, *args, **kwargs):
        instance = kwargs.get('instance')
        n_features = kwargs.get('n_features')

        if self.mode == 'classification':
            predict = self.model_to_understand.predict_proba
        elif self.mode == 'regression':
            predict = self.model_to_understand.predict
        else:
            raise ValueError(f'{self.__class__.__name__} class doesnt handle with {self.mode} type')

        if instance is not None and n_features:
            return self.explainer.explain_instance(instance,
                                                   predict,
                                                   num_features=n_features
                                                   )
        else:
            raise ValueError(f'{self._uai_generate_table.__name__} method '
                             f'in {self.__class__.__name__} class missing argument')