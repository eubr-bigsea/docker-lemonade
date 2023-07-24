import base64
from inspect import getmembers
from io import BytesIO
from sklearn.tree import plot_tree
import numpy as np
from matplotlib import pyplot as plt


class PltGenerate:

    def __init__(self, info_args):
        self.plot_dict = self.generate_plot_dict()
        self.info_args = info_args
        self.n_fig = len(info_args)
        self.fig_size = (12, 8) if self.n_fig == 2 else (8, 6)
        if 'dt_surface' in info_args:
            self.fig_size = (16, 12) if self.n_fig == 2 else (12, 10)

    def _plot_feature_importance(self, ax):
        values, names = self.info_args['feature_importance']
        ax.set_axisbelow(True)
        ax.grid()
        ax.bar(names, values)
        ax.set_xticks(np.arange(len(names)))
        ax.set_xticklabels(names, rotation=45)

    def _plot_dt_surface(self, ax):
        tree_dict = self.info_args['dt_surface']
        plot_tree(decision_tree=tree_dict['model'],
                  max_depth=tree_dict['max_deep'],
                  feature_names=tree_dict['feature_names'],
                  filled=True,
                  ax=ax)

    def _plot_forest_importance(self, ax):
        values, std, names = self.info_args['forest_importance']
        ax.set_axisbelow(True)
        ax.grid()
        ax.bar(names, values, yerr=std)
        ax.set_xticks(np.arange(len(names)))
        ax.set_xticklabels(names, rotation=45)

    def _plot_find_neighborhood(self, ax):
        x, y, c, idx = self.info_args['find_neighborhood']
        size = [25]*len(c)
        for i in idx[0:5]:
            size[i+1] = 100

        size[0] = 250

        ax.set_axisbelow(True)
        ax.grid()
        ax.scatter(x, y, c=c, s=size)

    def generate_plot_dict(self):
        members = getmembers(self)
        return {name.strip('_plot_'): member for name, member in members if name.startswith('_plot_')}

    def create_plots(self):
        fig, ax = plt.subplots(nrows=1, ncols=self.n_fig, figsize=self.fig_size, squeeze=False)
        ax = ax.reshape(-1)
        for i, xai_arg in enumerate(self.info_args):
            self.plot_dict[xai_arg](ax[i])
        fig_file = BytesIO()
        fig.savefig(fig_file, format='png')
        return base64.b64encode(fig_file.getvalue()).decode('utf-8')


