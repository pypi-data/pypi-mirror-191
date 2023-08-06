import numpy as np
from sklearn import datasets

def export_ml_simulation(data_R, data_S, features_R, n_informative):

    print('ml')
    features, output, coef = datasets.make_regression(n_samples = len(data_R), n_features = len(features_R),
        n_informative = n_informative, n_targets = 1,
        noise = 0.0, coef = True)

    print('features:\n', features)
    print('output:\n', output)
    print('coef:\n', coef)