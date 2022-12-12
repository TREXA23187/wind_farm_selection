from utils.show_factor import show_factors
from utils.gwr_grid_test import gwr_grid, plot_factors
from utils.gwr_ward_test import gwr_ward, plot_ward_factors

import matplotlib.pyplot as plt

if __name__ == '__main__':
    show_factors()
    plot_factors()
    gwr_grid(is_gwr_summary=False, is_plot_coefficient=True)
    plot_ward_factors()
    gwr_ward(is_gwr_summary=True, is_plot_coefficient=True)

    plt.show()
