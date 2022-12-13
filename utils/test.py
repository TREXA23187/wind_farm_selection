import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


def plot_examples(colormaps):
    """
    Helper function to plot data with associated colormap.
    """
    np.random.seed(19680801)
    data = np.random.randn(30, 30)
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                            constrained_layout=True, squeeze=False)
    for [ax, cmap] in zip(axs.flat, colormaps):
        # fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)
        # psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-1, vmax=1)
        fig.colorbar(cm.ScalarMappable(cmap=cmap), ax=ax, location='right')
        # fig.colorbar(mappable=psm,ax=ax,location='right')
    plt.show()


if __name__ == '__main__':
    cmap = ListedColormap(["darkorange", "gold", "lawngreen", "lightseagreen"])
    plot_examples([cmap])
