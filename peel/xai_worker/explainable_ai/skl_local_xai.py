from sklearn.neighbors import KNeighborsClassifier

from juicer.explainable_ai.noise_set import NoiseSet
from juicer.explainable_ai.interpretability import TreeInterpretation, LinearRegressionInterpretation, KNNInterpretation
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Ridge, LogisticRegression


class LocalXAI:

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 info_data=None,
                 noise_num_samples=2500,
                 type_noise='normal',
                 feature_names=None,
                 target_name=None):

        self.arguments_used = arguments_used
        self.model_to_understand = model_to_understand
        self.data_source = data_source
        self.info_data = info_data
        self.feature_names = feature_names
        self.target_name = target_name
        self.noise_num_samples = noise_num_samples
        self.type_noise = type_noise

    def create_noise_set(self, instance):
        if self.info_data is not None:
            ns = NoiseSet(num_samples=self.noise_num_samples, info_data=self.info_data)
        elif self.data_source is not None:
            ns = NoiseSet(num_samples=self.noise_num_samples, x_data=self.data_source)
        else:
            raise ValueError(f"{self.__class__.__name__} must define info_data or data_source")

        if self.type_noise == 'normal':
            ar = self.arguments_used.get("approach_rate")
            if ar is not None:
                return ns.normal_with_bias(instance=instance, approach_rate=ar)
            else:
                return ns.normal_with_bias(instance=instance)
        else:
            raise ValueError(f"{self.__class__.__name__} does not know how to handle with type_noise: {self.type_noise}")

    def local_explanation(self, instance):
        x_noise = self.create_noise_set(instance)
        y_noise = self.model_to_understand.predict(x_noise)

        local_method_type = self.arguments_used.get('local_method')

        if local_method_type == "dt_cls":
            local_args = self.arguments_used.get('local_args')
            local_method = DecisionTreeClassifier()
            local_method.fit(x_noise, y_noise)
            xai_tree = TreeInterpretation(arguments_used=local_args,
                                          model_to_understand=local_method,
                                          feature_names=self.feature_names)
            xai_tree.generate_arguments()
            return xai_tree.generated_args_dict

        elif local_method_type == "rf_cls":
            local_args = self.arguments_used.get('local_args')
            local_method = RandomForestClassifier()
            local_method.fit(x_noise, y_noise)
            xai_tree = TreeInterpretation(arguments_used=local_args,
                                          model_to_understand=local_method,
                                          feature_names=self.feature_names)
            xai_tree.generate_arguments()
            return xai_tree.generated_args_dict

        elif local_method_type == "rf_reg":
            local_args = self.arguments_used.get('local_args')
            local_method = RandomForestRegressor()
            local_method.fit(x_noise, y_noise)
            xai_tree = TreeInterpretation(arguments_used=local_args,
                                          model_to_understand=local_method,
                                          feature_names=self.feature_names)
            xai_tree.generate_arguments()
            return xai_tree.generated_args_dict

        elif local_method_type == "lreg":
            local_args = self.arguments_used.get('local_args')
            local_method = Ridge(alpha=2)
            local_method.fit(x_noise, y_noise)
            xai_tree = LinearRegressionInterpretation(arguments_used=local_args,
                                                      model_to_understand=local_method,
                                                      feature_names=self.feature_names)
            xai_tree.generate_arguments()
            return xai_tree.generated_args_dict

        elif local_method_type == "logit":
            local_args = self.arguments_used.get('local_args')
            local_method = LogisticRegression(max_iter=1000, tol=1e-1, )
            local_method.fit(x_noise, y_noise)
            xai_tree = LinearRegressionInterpretation(arguments_used=local_args,
                                                      model_to_understand=local_method,
                                                      feature_names=self.feature_names)
            xai_tree.generate_arguments()
            return xai_tree.generated_args_dict

        else:
            raise ValueError(f"{self.__class__.__name__} does not how to "
                             f"handle with local method {local_method_type}")







