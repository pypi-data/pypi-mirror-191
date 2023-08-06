import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from evalAIRR.util.univar import get_feature_data

from copulas.univariate import Univariate
from copulas.multivariate import GaussianMultivariate
from copulas.visualization import compare_2d, compare_3d

import warnings
warnings.filterwarnings("ignore")

def export_copula_2d_scatter_plot(feature_1, feature_2, data_R, data_S, features_R, features_S):
    data_R_f1 = get_feature_data(feature_1, data_R, features_R)
    data_R_f2 = get_feature_data(feature_2, data_R, features_R)
    if not any(data_R_f1) or not any(data_R_f2):
        return

    data_S_f1 = get_feature_data(feature_1, data_S, features_S)
    data_S_f2 = get_feature_data(feature_2, data_S, features_S)
    if not any(data_R_f2) or not any(data_S_f2):
        return

    data_R_join = np.stack((data_R_f1, data_R_f2)).T
    data_S_join = np.stack((data_S_f1, data_S_f2)).T

    univariate = Univariate()
    univariate.fit(data_R_f1)
    data_R_f1_dist = univariate.to_dict()['type']
    univariate.fit(data_R_f2)
    data_R_f2_dist = univariate.to_dict()['type']
    univariate.fit(data_S_f1)
    data_S_f1_dist = univariate.to_dict()['type']
    univariate.fit(data_S_f2)
    data_S_f2_dist = univariate.to_dict()['type']

    dist_R = GaussianMultivariate(distribution={
        feature_1: data_R_f1_dist,
        feature_2: data_R_f2_dist
    })
    d_R = { feature_1: data_R_join[:, 0], feature_2: data_R_join[:, 1] }
    df_R = pd.DataFrame(data=d_R)
    dist_R.fit(df_R)

    dist_S = GaussianMultivariate(distribution={
        feature_1: data_S_f1_dist,
        feature_2: data_S_f2_dist
    })
    d_S = { feature_1: data_S_join[:, 0], feature_2: data_S_join[:, 1] }
    df_S = pd.DataFrame(data=d_S)
    dist_S.fit(df_S)

    compare_2d(df_R, df_S)
    plt.suptitle(f'Distribution of {feature_1} and {feature_2} in copula space')
    plt.savefig(f'./output/temp_figures/copula_2d_plot_{feature_1}_{feature_2}.svg')
    plt.close()

def export_copula_3d_scatter_plot(feature_1, feature_2, feature_3, data_R, data_S, features_R, features_S):
    data_R_f1 = get_feature_data(feature_1, data_R, features_R)
    data_R_f2 = get_feature_data(feature_2, data_R, features_R)
    data_R_f3 = get_feature_data(feature_3, data_R, features_R)
    if not any(data_R_f1) or not any(data_R_f2) or not any(data_R_f3):
        return

    data_S_f1 = get_feature_data(feature_1, data_S, features_S)
    data_S_f2 = get_feature_data(feature_2, data_S, features_S)
    data_S_f3 = get_feature_data(feature_3, data_S, features_S)
    if not any(data_R_f2) or not any(data_S_f2) or not any(data_S_f3):
        return

    data_R_join = np.stack((data_R_f1, data_R_f2, data_R_f3)).T
    data_S_join = np.stack((data_S_f1, data_S_f2, data_S_f3)).T

    univariate = Univariate()
    univariate.fit(data_R_f1)
    data_R_f1_dist = univariate.to_dict()['type']
    univariate.fit(data_R_f2)
    data_R_f2_dist = univariate.to_dict()['type']
    univariate.fit(data_R_f3)
    data_R_f3_dist = univariate.to_dict()['type']
    univariate.fit(data_S_f1)
    data_S_f1_dist = univariate.to_dict()['type']
    univariate.fit(data_S_f2)
    data_S_f2_dist = univariate.to_dict()['type']
    univariate.fit(data_S_f3)
    data_S_f3_dist = univariate.to_dict()['type']

    dist_R = GaussianMultivariate(distribution={
        feature_1: data_R_f1_dist,
        feature_2: data_R_f2_dist,
        feature_3: data_R_f3_dist
    })
    d_R = { 
        feature_1: data_R_join[:, 0], 
        feature_2: data_R_join[:, 1], 
        feature_3: data_R_join[:, 2] 
    }
    df_R = pd.DataFrame(data=d_R)
    dist_R.fit(df_R)

    dist_S = GaussianMultivariate(distribution={
        feature_1: data_S_f1_dist,
        feature_2: data_S_f2_dist,
        feature_3: data_S_f3_dist
    })
    d_S = { 
        feature_1: data_S_join[:, 0], 
        feature_2: data_S_join[:, 1], 
        feature_3: data_S_join[:, 2] 
    }
    df_S = pd.DataFrame(data=d_S)
    dist_S.fit(df_S)

    compare_3d(df_R, df_S, columns=[feature_1, feature_2, feature_3], figsize=(10, 5))
    fig = plt.gcf()
    fig.suptitle(f'Distribution of {feature_1}, {feature_2} and {feature_3} in copula space')
    for ax in fig.axes:
        ax.set_xlabel(feature_1)
        ax.set_ylabel(feature_2)
        ax.set_zlabel(feature_3)
    fig.tight_layout()
    fig.savefig(f'./output/temp_figures/copula_3d_plot_{feature_1}_{feature_2}_{feature_3}.svg')
    del fig
    plt.close()