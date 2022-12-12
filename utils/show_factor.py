import geopandas
import geopandas as gpd
import pandas
from shapely import geometry
from osgeo import gdal
import rasterio
from rasterio import plot as raster_plot
import matplotlib.pyplot as plt

from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm, \
    temperature, precipitation, population, slope, aspect, land_use, wind_speed, road

STATIC_CRS = 'epsg:27700'

legend_kwd = {'loc': 'lower right',
              'markerscale': 0.29,
              'title_fontsize': 'small',
              'fontsize': 'xx-small'}


def show_factors():
    fig, axis = plt.subplots(nrows=3, ncols=4, figsize=(12, 7), dpi=100)
    fig.suptitle('Factors')

    ax1 = axis[0, 0]
    ax2 = axis[0, 1]
    ax3 = axis[0, 2]
    ax4 = axis[0, 3]
    ax5 = axis[1, 0]
    ax6 = axis[1, 1]
    ax7 = axis[1, 2]
    ax8 = axis[1, 3]
    ax9 = axis[2, 0]
    ax10 = axis[2, 1]
    ax11 = axis[2, 2]
    ax12 = axis[2, 3]

    ax1.set_title('existing wind farm')
    ax1.set_axis_off()
    wind_farm.to_crs(STATIC_CRS).plot(ax=ax1, color='red')
    south_scotland.to_crs(STATIC_CRS).plot(ax=ax1, alpha=.2, color='orange')

    ax2.set_title('conservation')
    ax2.set_axis_off()
    conservation.plot(ax=ax2, color='green')
    south_scotland.plot(ax=ax2, alpha=.5, color='green')

    ax3.set_title('residential area')
    ax3.set_axis_off()
    south_scotland.plot(ax=ax3, color='lightblue')
    scotland_residence.plot(ax=ax3, markersize=1, color='blue')

    ax4.set_title('power station')
    ax4.set_axis_off()
    scotland_power_station.plot(ax=ax4, markersize=1, color='grey', alpha=.8)
    south_scotland.plot(ax=ax4, alpha=.5, color='grey')

    ax5.set_title('temperature')
    ax5.set_axis_off()
    temperature.plot(ax=ax5, column='aveTemp', cmap='Reds', scheme='NaturalBreaks', k=6, legend=True,
                     legend_kwds=legend_kwd)

    ax6.set_title('land use')
    ax6.set_axis_off()
    raster_plot.show(
        land_use,
        ax=ax6,
        cmap='gist_ncar',
        # alpha=.7
    )

    ax7.set_title('slope')
    ax7.set_axis_off()
    raster_plot.show(
        slope,
        ax=ax7,
        # alpha=.7,
        cmap='terrain'
    )

    ax8.set_title('aspect')
    ax8.set_axis_off()
    raster_plot.show(
        aspect,
        ax=ax8,
        # alpha=.8,
        cmap='Greys'
    )

    ax10.set_title('wind speed')
    ax10.set_axis_off()
    raster_plot.show(
        wind_speed,
        ax=ax10,
        # alpha=.8,
        cmap='YlGnBu'
    )

    ax9.set_title('population')
    ax9.set_axis_off()
    population.plot(ax=ax9, column='SSP1_2020', cmap='Oranges', scheme='NaturalBreaks', k=3)

    ax11.set_title('precipitation')
    ax11.set_axis_off()
    precipitation.plot(ax=ax11, column='prSum', cmap='PuBu', scheme='NaturalBreaks', k=6)

    ax12.set_title('road')
    ax12.set_axis_off()
    road.to_crs(STATIC_CRS).plot(ax=ax12, linewidth=1, alpha=0.8, color='grey')
    south_scotland.to_crs(STATIC_CRS).plot(ax=ax12, alpha=.2, color='grey')


if __name__ == '__main__':
    show_factors()

    plt.show()
