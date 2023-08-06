import numpy as np
import os
import matplotlib.pyplot as plt
from simba.unsupervised.misc import (read_pickle,
                                     check_directory_exists,
                                     check_that_directory_is_empty,
                                     find_embedding)
import pandas as pd

class GridSearchVisualizer(object):
    def __init__(self,
                 embedders_path: str,
                 clusterers_path: str or None,
                 save_dir: str,
                 settings: dict):

        check_directory_exists(embedders_path)
        check_directory_exists(save_dir)
        self.save_dir = save_dir
        self.embedders_path = embedders_path
        self.settings = settings
        self.clusterers = None
        if clusterers_path:
            self.clusterers = read_pickle(data_path=clusterers_path)

    def create_datasets(self):
        self.img_data = {}
        print('Retrieving models for visualization...')
        self.embedders = read_pickle(data_path=self.embedders_path)
        if self.clusterers:
            for k, v in self.clusterers.items():
                self.img_data[k] = {}
                self.img_data[k]['categorical_legends'] = set()
                self.img_data[k]['continuous_legends'] = set()
                embedder = find_embedding(embeddings=self.embedders, hash=v['HASH'])
                cluster_data = v['model'].labels_.reshape(-1, 1).astype(np.int8)
                embedding_data = embedder['models'].embedding_
                data = np.hstack((embedding_data, cluster_data))
                self.img_data[k]['data'] = pd.DataFrame(data, columns=['X', 'Y', 'CLUSTER'])
                self.img_data[k]['HASH'] = v['HASH']
                self.img_data[k]['CLUSTERER_NAME'] = v['NAME']
                self.img_data[k]['categorical_legends'].add('CLUSTER')
        else:
            for k, v in self.embedders.items():
                self.img_data[k] = {}
                embedding_data = v['models'].embedding_
                self.img_data[k]['data'] = pd.DataFrame(embedding_data, columns=['X', 'Y'])
                self.img_data[k]['HASH'] = v['HASH']

        if self.settings['HUE']:
            for hue_id, hue_settings in self.settings['HUE'].items():
                field_type, field_name  = hue_settings['FIELD_TYPE'], hue_settings['FIELD_NAME']
                for k, v in self.img_data.items():
                    embedder = self.__find_embedding(self.img_data[k]['HASH'])
                    if not 'categorical_legends' in self.img_data[k].keys():
                        self.img_data[k]['categorical_legends'] = set()
                        self.img_data[k]['continuous_legends'] = set()
                    if (field_type == 'CLASSIFIER') or (field_type == 'VIDEO_NAMES'):
                        if field_name:
                            self.img_data[k]['categorical_legends'].add(field_name)
                        else:
                            self.img_data[k]['categorical_legends'].add(field_type)
                    elif (field_type == 'CLASSIFIER_PROBABILITY') or (field_type == 'FRAME_IDS'):
                        if field_name:
                            self.img_data[k]['continuous_legends'].add(field_name)
                        else:
                            self.img_data[k]['continuous_legends'].add(field_type)
                    if field_name:
                        self.img_data[k]['data'][field_name] = embedder[field_type][field_name]
                    else:
                        self.img_data[k]['data'][field_type] = embedder[field_type]

    def create_imgs(self):
        print('Creating plots...')
        plots = {}
        for k, v in self.img_data.items():
            for categorical in v['categorical_legends']:
                fig, ax = plt.subplots()
                colmap = {name: n for n, name in enumerate(set(list(v['data'][categorical].unique())))}
                scatter = ax.scatter(v['data']['X'], v['data']['Y'], c=[colmap[name] for name in v['data'][categorical]], cmap=self.settings['CATEGORICAL_PALETTE'], s=self.settings['SCATTER_SIZE'])
                plt.legend(*scatter.legend_elements()).set_title(categorical)
                plt.xlabel('X')
                plt.ylabel('Y')
                if categorical != 'CLUSTER':
                    plt_key = v['HASH'] + '_' + categorical
                    title = 'EMBEDDER: {}'.format(v['HASH'])
                    plt.title(title, ha="center", fontsize=15, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 0})
                else:
                    plt_key = v['HASH'] + '_' + v['CLUSTERER_NAME']
                    title = 'EMBEDDER: {} \n CLUSTERER: {}'.format(v['HASH'], v['CLUSTERER_NAME'])
                    plt.title(title, ha="center", fontsize=15, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 0})
                plots[plt_key] = fig
                plt.close('all')

            for continuous in v['continuous_legends']:
                fig, ax = plt.subplots()
                plt.xlabel('X')
                plt.ylabel('Y')
                points = ax.scatter(v['data']['X'], v['data']['Y'], c=v['data'][continuous], s=self.settings['SCATTER_SIZE'], cmap=self.settings['CONTINUOUS_PALETTE'])
                cbar = fig.colorbar(points)
                cbar.set_label(continuous, loc='center')
                plt_key = v['HASH'] + '_' + continuous
                title = 'EMBEDDER: {}'.format(v['HASH'])
                plt.title(title, ha="center", fontsize=15, bbox={"facecolor": "orange", "alpha": 0.5, "pad": 0})
                plots[plt_key] = fig
                plt.close('all')

        for plt_key, fig in plots.items():
            save_path = os.path.join(self.save_dir, f'{plt_key}.png')
            print(f'Saving scatterplot {plt_key} ...')
            fig.savefig(save_path)

# settings = {'HUE': {'FIELD_TYPE': 'VIDEO_NAMES', 'FIELD_NAME': None}}
# settings = {'SCATTER_SIZE': 50, 'CATEGORICAL_PALETTE': 'Set1', 'CONTINUOUS_PALETTE': 'magma', 'HUE': {0: {'FIELD_TYPE': 'FRAME_IDS', 'FIELD_NAME': None}, 1: {'FIELD_TYPE': 'CLF', 'FIELD_NAME': 'Attack'}}}
# test = GridSearchVisualizer(embedders_path='/Users/simon/Desktop/envs/troubleshooting/unsupervised/dr_models',
#                             clusterers_path= '/Users/simon/Desktop/envs/troubleshooting/unsupervised/cluster_models',
#                             save_dir='/Users/simon/Desktop/envs/troubleshooting/unsupervised/images',
#                             settings=settings)
# test.create_datasets()
# test.create_imgs()
