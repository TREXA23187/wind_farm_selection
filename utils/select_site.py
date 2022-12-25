import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS

from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm, \
    temperature, precipitation, population, road, community_council, landscape

CRS_4326 = CRS('epsg:4326')
STATIC_CRS = CRS('epsg:27700')


def plot_sample():
    fig_base = plt.figure(figsize=(4, 7), dpi=100)
    ax = fig_base.add_subplot(111)
    ax.set_axis_off()

    south_scotland.to_crs(STATIC_CRS).plot(ax=ax, figsize=(10, 10), facecolor='None', edgecolor='Black')
    scotland_power_station.to_crs(STATIC_CRS).buffer(5000).plot(ax=ax, color='blue', alpha=.2)
    conservation.to_crs(STATIC_CRS).buffer(5000).plot(ax=ax, color='blue', alpha=.2)
    road.to_crs(STATIC_CRS).buffer(5000).plot(ax=ax, color='blue', alpha=.2)

    power_station_buffer = scotland_power_station.to_crs(STATIC_CRS).buffer(5000)
    conservation_buffer = conservation.to_crs(STATIC_CRS).buffer(5000)
    road_buffer = road.to_crs(STATIC_CRS).buffer(5000)

    power_station_buffer_df = gpd.GeoDataFrame(power_station_buffer, columns=['geometry'])

    conservation_buffer_df = gpd.GeoDataFrame(conservation_buffer, columns=['geometry'])
    road_buffer_df = gpd.GeoDataFrame(road_buffer, columns=['geometry'])

    res = gpd.sjoin(power_station_buffer_df, conservation_buffer_df)

    print(res)
    # gpd.sjoin(res, road_buffer_df).plot()


if __name__ == '__main__':
    plot_sample()

    plt.show()
