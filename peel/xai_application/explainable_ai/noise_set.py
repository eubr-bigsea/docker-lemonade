import numpy as np
import pandas as pd


class NoiseSet:

    def __init__(self, num_samples,  x_data=None, info_data=None):
        self.num_samples = num_samples
        self.x_data = x_data
        self.info_data = info_data

    @property
    def x_data(self):
        return self._x_data

    @x_data.setter
    def x_data(self, x_data):
        if isinstance(x_data, pd.DataFrame):
            self._x_data = x_data
        else:
            raise ValueError(f"class {self.__class__.__name__} just accept pandas DataFrame")

    @property
    def info_data(self):
        return self._info_data

    @info_data.setter
    def info_data(self, info_data):
        if self.x_data is not None and info_data is None:
            data_mean = self.x_data.mean()
            data_std = self.x_data.std()
            min_data = self.x_data.min()
            max_data = self.x_data.max()
            self._info_data = {"mean": data_mean,
                               "std": data_std,
                               "min": min_data,
                               "max": max_data}
        else:
            self._info_data = info_data

    def normal_with_bias(self, instance, scale=None, approach_rate=0.15):
        if scale is not None:
            noise_set = np.random.normal(instance,
                                         scale=scale*approach_rate,
                                         size=(self.num_samples, len(instance)))
        elif self.info_data is not None:
            noise_set = np.random.normal(instance,
                                         scale=self.info_data['std']*approach_rate,
                                         size=(self.num_samples, len(instance)))
        else:
            raise ValueError(f"class {self.__class__.__name__} must have info_data "
                             f"different to None or pass scale parameter")

        max_, min_ = self.info_data.get('max').values, self.info_data.get('min').values
        if max_ is not None and min_ is not None:
            noise_set = np.clip(noise_set, min_, max_)

        return noise_set

    def uniform_distance(self, instance, min_values=None, max_values=None):

        if min_values is not None and max_values is not None:
            uniform_data = np.random.uniform(low=min_values, high=max_values, size=(self.num_samples, len(instance)))
        elif self.info_data is not None:
            i = self.info_data.get('min').values
            a = self.info_data.get('max').values
            if i is not None and a is not None:
                uniform_data = np.random.uniform(low=i, high=a, size=(self.num_samples, len(instance)))
            else:
                raise ValueError(f"class {self.__class__.__name__} must have info_data "
                                 f"different to None or pass min and max values as  parameter")
        else:
            raise ValueError(f"class {self.__class__.__name__} must have info_data "
                             f"different to None or pass min and max values as  parameter")

        distances = np.linalg.norm(uniform_data - instance, axis=1)

        return uniform_data, distances
