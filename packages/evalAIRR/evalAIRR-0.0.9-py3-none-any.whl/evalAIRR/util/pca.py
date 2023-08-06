import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def pca(A,m):
    pca = PCA(n_components=m, copy=True)
    pca.fit(A)
    return pca.explained_variance_, pca.transform(A)

def export_pca_2d_comparison(data_real, data_sim):
    _, pca_R = pca(data_real, 2)
    _, pca_S = pca(data_sim, 2)

    f, ax = plt.subplots(1, 1)
    f.set_size_inches(5, 5)
    f.suptitle('Real and simulated dataset comparison\nin two dimensions using PCA')
    ax.scatter(pca_R[:, 0], pca_R[:, 1], label='Real')
    ax.scatter(pca_S[:, 0], pca_S[:, 1], c='red', label='Simulated')
    ax.legend()
    f.tight_layout()
    # ax2.set_ylabel('')
    # ax2.set_yticklabels([])
    # ax2.set_yticks([])

    f.savefig(f'./output/temp_figures/pca_2d_comparison.svg')
    del f
    plt.close()