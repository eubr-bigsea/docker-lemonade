import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import norm
from sklearn.metrics import mean_squared_error

from explainable_ai.understand_ai import Understanding


class Interpretation(Understanding):

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 feature_names=None,
                 target_name=None,
                 feature_importance=None):

        """

        :param arguments_used:
        :param model_to_understand:
        :param data_source:
        :param feature_names:
        :param target_name:
        :param feature_importance:
        """

        super().__init__(arguments_used, model_to_understand, data_source, feature_names, target_name)
        self.feature_importance = feature_importance

    @property
    def feature_importance(self):
        return self._feature_importance

    @feature_importance.setter
    def feature_importance(self, feature_importance):
        if feature_importance is not None:
            self._feature_importance = feature_importance
        elif self.model_to_understand is not None:
            if hasattr(self.model_to_understand, 'feature_importances_'):
                self._feature_importance = self.model_to_understand.feature_importances_
            elif hasattr(self.model_to_understand, 'coef_'):
                self._feature_importance = self.model_to_understand.coef_
            else:
                raise ValueError(f'Model {self.model_to_understand.__class__.__name__} does not have'
                                 f'interpretable attribute in {self.__class__.__name__}')
        else:
            raise ValueError(f'{self.__class__.__name__} class does not find feature importance.')

    def _uai_feature_importance(self, *args, **kwargs):
        n_feature = kwargs.get('n_feature')
        if n_feature:
            sorted_idx = np.argsort(self.feature_importance)[::-1]
            n_imp = [self.feature_importance[i] for i in sorted_idx[:n_feature]]
            n_names = [self.feature_names[i] for i in sorted_idx[:n_feature]]
            return n_imp, n_names
        else:
            return self.feature_importance, self.feature_names


class TreeInterpretation(Interpretation):

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 feature_names=None,
                 target_name=None,
                 feature_importance=None):
        super().__init__(arguments_used,
                         model_to_understand,
                         data_source,
                         feature_names,
                         target_name,
                         feature_importance)

    def _uai_dt_surface(self, *args, **kwargs):
        max_deep = kwargs.get('max_deep')
        return {'feature_names': self.feature_names,
                'max_deep': max_deep,
                'model': self.model_to_understand}


class EnsembleInterpretation(Interpretation):

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 feature_names=None,
                 target_name=None,
                 feature_importance=None):
        super().__init__(arguments_used,
                         model_to_understand,
                         data_source,
                         feature_names,
                         target_name,
                         feature_importance)

    def _uai_forest_importance(self, *args, **kwargs):
        n_feature = kwargs.get('n_feature')
        std = np.std([tree.feature_importances_ for tree in self.model_to_understand.estimators_], axis=0)
        if n_feature:
            sorted_idx = np.argsort(self.feature_importance)[::-1]
            n_std = [std[i] for i in sorted_idx[:n_feature]]
            n_imp = [self.feature_importance[i] for i in sorted_idx[:n_feature]]
            n_names = [self.feature_names[i] for i in sorted_idx[:n_feature]]
            return n_imp, n_std, n_names
        else:
            return self.feature_importance, std, self.feature_names


class LinearRegressionInterpretation(Interpretation):

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 feature_names=None,
                 target_name=None,
                 feature_importance=None):

        super().__init__(arguments_used,
                         model_to_understand,
                         data_source,
                         feature_names,
                         target_name,
                         feature_importance)

    def _uai_p_value(self, *args, **kwargs):
        if self.data_source is not None:
            X = self.data_source[self.feature_names[:-1]].values
            if self.target_name:
                y = self.data_source[self.target_name].values
            else:
                y = self.data_source.iloc[:, -1:].values.reshape(1, -1)[0]
        else:
            raise ValueError(f'{self.__class__.__name__} class must have a data source in order to calculate p-value.')

        if self.model_to_understand:
            coef = np.append(self.model_to_understand.intercept_, self.model_to_understand.coef_)
            X = np.append(np.ones((len(X), 1)), X, axis=1)
        else:
            raise ValueError(f'{self.__class__.__name__} class must have a model')

        predictions = self.model_to_understand.predict(self.data_source[self.feature_names[:-1]])
        mse = mean_squared_error(y, predictions)
        var_b = mse*(np.linalg.pinv(np.dot(X.T, X)).diagonal())
        sd_b = np.sqrt(var_b)
        ts_b = coef/sd_b
        p_values = [2 * (1 - stats.t.cdf(np.abs(i), (len(X) - len(X[0])))) for i in ts_b]

        return pd.DataFrame({
            "Coefficients": np.round(coef, 4),
            "Standard Errors": np.round(sd_b, 3),
            't_values': np.round(ts_b, 3),
            'p_values': np.round(p_values, 3)
        })


class LogisticRegressionInterpretation(Interpretation):

    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 feature_names=None,
                 target_name=None,
                 feature_importance=None):

        super().__init__(arguments_used,
                         model_to_understand,
                         data_source,
                         feature_names,
                         target_name,
                         feature_importance)

    def _uai_feature_importance(self, *args, **kwargs):
        n_feature = kwargs.get('n_feature')
        if n_feature:
            sorted_idx = np.argsort(self.feature_importance[0])[::-1]
            n_imp = [self.feature_importance[0][i] for i in sorted_idx[:n_feature]]
            n_names = [self.feature_names[i] for i in sorted_idx[:n_feature]]
            return n_imp, n_names
        else:
            return self.feature_importance[0], self.feature_names

    def statistic_logit(self):
        coef = np.append(self.model_to_understand.intercept_, self.model_to_understand.coef_)
        x = self.data_source[self.feature_names].values
        X = np.column_stack((np.ones(x.shape[0]), x))

        n, p = X.shape
        denom = 2 * (1 + np.cosh(self.model_to_understand.decision_function(x)))
        denom = np.tile(denom, (p, 1)).T
        fim = (X / denom).T @ X
        crao = np.linalg.pinv(fim)
        se = np.sqrt(np.diag(crao))
        z_scores = coef / se

        # Two-tailed p-values
        pval = 2 * norm.sf(np.fabs(z_scores))

        crit = norm.ppf(1 - 0.05 / 2)
        ll = coef - crit * se
        ul = coef + crit * se

        # Rename CI
        ll_name = "CI[%.1f%%]" % (100 * 0.05 / 2)
        ul_name = "CI[%.1f%%]" % (100 * (1 - 0.05 / 2))
        f_names = [name for name in self.feature_names]
        f_names.insert(0, 'intercept')
        # Create dict
        stats = {
            "names": f_names,
            "coef": coef,
            "se": se,
            "z": z_scores,
            "pval": pval,
            "ll_name": ll,
            "ul_name": ul,
        }

        return stats

class KNNInterpretation(Interpretation):
    def __init__(self,
                 arguments_used,
                 model_to_understand=None,
                 data_source=None,
                 feature_names=None,
                 target_name=None,
                 feature_importance=False):

        super().__init__(arguments_used,
                         model_to_understand,
                         data_source,
                         feature_names,
                         target_name,
                         feature_importance)

        self.target = self.data_source.iloc[:, -1:].values.reshape(1, -1)[0]

    def _uai_feature_importance(self, *args, **kwargs):
        raise NotImplementedError("There isn't feature importance in KNN")

    def _distance_representation(self, instance):
        d, idx = self.model_to_understand.kneighbors(X=instance.reshape(1, -1), n_neighbors=20)
        v = [v / np.max(d) * 5 for v in d[0][1:]]
        radius = np.array(v, dtype=float)
        angle = np.linspace(0.1, np.pi, 19)
        color = self.target[idx]
        aux = np.argsort(color[0][1:])
        c = color[0][1:]
        c = np.array(c[aux])

        x_c = [r * np.cos(t) for r, t in zip(radius[aux], angle)]
        y_c = [r * np.sin(t) for r, t in zip(radius[aux], angle)]

        x_c.insert(0, 0)
        y_c.insert(0, 0)
        c = np.insert(c, 0, self.model_to_understand.predict(instance.reshape(1, -1)))

        return x_c, y_c, c, np.argsort(aux)

    def _uai_find_neighborhood(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None:
            return self._distance_representation(instance)
        else:
            raise ValueError(f'{self.__class__.__name__} doesnt '
                             f'handle with {type(instance)} as instance')














