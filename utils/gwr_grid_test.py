import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS

from mgwr.gwr import GWR
from spreg.ml_lag import ML_Lag
from spreg.ml_error import ML_Error

from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm, \
    temperature, precipitation, population, road, community_council, landscape

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# pd.set_option('display.max_rows', None)

CRS_4326 = CRS('epsg:4326')
STATIC_CRS = CRS('epsg:27700')

GRID_NUM = 32


def generate_grid():
    x = np.linspace(195874, 398018, GRID_NUM)
    y = np.linspace(530251, 687573, GRID_NUM)
    grid = []
    for m, i in enumerate(x[:GRID_NUM - 1]):
        for k, j in enumerate(y[:GRID_NUM - 1]):
            cord = np.array([i, j, x[m + 1], j, x[m + 1], y[k + 1], i, y[k + 1]]).reshape(4, 2)
            grid.append(Polygon(cord))

    area = gpd.GeoDataFrame(grid)
    area = area.reset_index()
    area.columns = ['index', 'geometry']
    area.crs = STATIC_CRS
    return area


def get_contain_point(name, right_df, contain_grid=generate_grid()):
    residence_join = gpd.sjoin(left_df=contain_grid, right_df=right_df.to_crs(STATIC_CRS), op='contains').groupby(
        'index')[
        'id'].count().to_frame().reset_index()
    contain_grid = pd.merge(contain_grid, residence_join, on='index', how='outer')
    contain_grid['id'] = contain_grid['id'].fillna(0)
    contain_grid.columns = ['index', 'geometry', f'{name}_result']

    return contain_grid


def get_overlay_area(name, df2, result_column=None):
    overlay_grid = generate_grid()

    overlay_result = gpd.overlay(df1=overlay_grid, df2=df2.to_crs(STATIC_CRS), how='intersection')
    overlay_result[f'{name}_result'] = overlay_result[result_column] if result_column else overlay_result.area / 10000
    overlay_result = pd.merge(overlay_grid, overlay_result, on='index', how='left')

    arr = [0 for _ in range((GRID_NUM - 1) ** 2)]

    for i in range(overlay_result.shape[0]):
        index = overlay_result.loc[i, 'index']
        value = overlay_result.loc[i, f'{name}_result']
        arr[index] += value

    overlay_grid[f'{name}_result'] = arr
    overlay_grid[f'{name}_result'] = overlay_grid[f'{name}_result'].fillna(0.0)
    overlay_grid.rename(columns={'geometry_x': 'geometry'}, inplace=True)

    return overlay_grid


def get_overlay_line(name, df2):
    overlay_line_grid = generate_grid()

    overlay_line_result = gpd.overlay(df1=overlay_line_grid, df2=df2.to_crs(STATIC_CRS), keep_geom_type=False)
    overlay_line_result[f'{name}_result'] = overlay_line_result.length
    overlay_line_result = pd.merge(overlay_line_grid, overlay_line_result, on='index', how='left')

    array = [0 for _ in range((GRID_NUM - 1) ** 2)]

    for i in range(overlay_line_result.shape[0]):
        index = overlay_line_result.loc[i, 'index']
        value = overlay_line_result.loc[i, f'{name}_result']
        array[index] += value

    overlay_line_grid[f'{name}_result'] = array
    overlay_line_grid[f'{name}_result'] = overlay_line_grid[f'{name}_result'].fillna(0.0)

    return overlay_line_grid


def plot_axis_grid(name, ax, display_grid=None):
    ax.set_title(name)
    ax.set_axis_off()
    if display_grid is not None:
        display_grid.plot(ax=ax, column=f'{name}_result', cmap='YlOrRd', edgecolor='Black', legend=True, linewidth=.5)


def plot_sample():
    sample_grid = generate_grid()
    fig_base = plt.figure(figsize=(4, 7), dpi=100)
    ax = fig_base.add_subplot(111)
    ax.set_axis_off()

    south_scotland.to_crs(STATIC_CRS).plot(ax=ax, figsize=(10, 10), facecolor='None', edgecolor='Black')
    sample_grid.plot(ax=ax, facecolor='None', edgecolor='red')
    scotland_residence.to_crs(STATIC_CRS).plot(ax=ax, markersize=1, color='blue')


def plot_factors():
    fig, axis = plt.subplots(nrows=3, ncols=4, figsize=(12, 7), dpi=100)
    fig.suptitle('Grid Factors Input')

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

    residence_grid = get_contain_point('residence', scotland_residence)

    scotland_power_station['id'] = scotland_power_station.index
    power_station_grid = get_contain_point('power_station', scotland_power_station)

    conservation_overlay_grid = get_overlay_area('conservation', conservation)
    wind_farm_overlay_grid = get_overlay_area('wind_farm', wind_farm)
    temperature_overlay_grid = get_overlay_area('temperature', temperature, result_column='aveTemp')
    precipitation_overlay_grid = get_overlay_area('precipitation', precipitation, result_column='prSum')
    population_overlay_grid = get_overlay_area('population', population, result_column='SSP1_2020')
    landscape_grid = get_overlay_area('landscape', landscape)

    road_overlay_grid = get_overlay_line('road', road)
    community_council_grid = get_overlay_line('community_council', community_council)

    # plot
    plot_axis_grid('wind_farm', ax1, wind_farm_overlay_grid)
    plot_axis_grid('residence', ax2, residence_grid)
    plot_axis_grid('power_station', ax3, power_station_grid)
    plot_axis_grid('conservation', ax4, conservation_overlay_grid)
    plot_axis_grid('temperature', ax5, temperature_overlay_grid)
    plot_axis_grid('precipitation', ax6, precipitation_overlay_grid)
    plot_axis_grid('population', ax7, population_overlay_grid)
    plot_axis_grid('road', ax8, road_overlay_grid)
    plot_axis_grid('community_council', ax9, community_council_grid)
    plot_axis_grid('landscape', ax10, landscape_grid)
    plot_axis_grid('landscape', ax11, landscape_grid)
    plot_axis_grid('landscape', ax12, landscape_grid)


def plot_coefficient(geo_data, cof_data_column, gwr_filter_t):
    fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(12, 7))
    axes = ax.flatten()
    fig.suptitle('Grid Factors Coefficient Output')

    for i in range(0, len(cof_data_column)):
        ax = axes[i]
        ax.set_title(cof_data_column[i])
        geo_data.plot(ax=ax, column=cof_data_column[i], edgecolor='white', cmap='Blues', legend=True)

        if (gwr_filter_t[i] == 0).any():
            geo_data[gwr_filter_t[i] == 0].plot(color='lightgrey', ax=ax, edgecolor='white')  # while grey is not

    for i in range(0, len(axes)):
        ax = axes[i]
        ax.set_axis_off()


def gwr(coordinates, y, x):
    # gwr_selector = Sel_BW(coordinates, y, x)
    # gwr_bw = gwr_selector.search(search_method='golden_section', criterion='AICc')
    # print('best gwr：', gwr_bw)

    gwr_results = GWR(coordinates, y, x, bw=44, fixed=False, kernel='gaussian', constant=True, spherical=True).fit()

    return gwr_results


def merge_columns(merge_data_list, merge_data_column):
    merge_result = generate_grid()

    for i in range(len(merge_data_list)):
        col = merge_data_column[i]
        merge_result = pd.merge(merge_result, merge_data_list[i][['index', col]], on='index')

    return merge_result


def gwr_grid(is_gwr_summary=False, is_plot_coefficient=False):
    residence_grid = get_contain_point('residence', scotland_residence)

    scotland_power_station['id'] = scotland_power_station.index
    power_station_grid = get_contain_point('power_station', scotland_power_station)

    conservation_overlay_grid = get_overlay_area('conservation', conservation)
    wind_farm_overlay_grid = get_overlay_area('wind_farm', wind_farm)
    temperature_overlay_grid = get_overlay_area('temperature', temperature, result_column='aveTemp')
    precipitation_overlay_grid = get_overlay_area('precipitation', precipitation, result_column='prSum')
    population_overlay_grid = get_overlay_area('population', population, 'SSP1_2020')
    landscape_grid = get_overlay_area('landscape', landscape)

    road_overlay_grid = get_overlay_line('road', road)
    community_council_grid = get_overlay_line('community_council', community_council)

    merge_data_list = [residence_grid, power_station_grid, conservation_overlay_grid, temperature_overlay_grid,
                       precipitation_overlay_grid, population_overlay_grid, landscape_grid, road_overlay_grid,
                       community_council_grid]
    merge_data_column = ['residence_result', 'power_station_result', 'conservation_result', 'temperature_result',
                         'precipitation_result', 'population_result', 'landscape_result', 'road_result',
                         'community_council_result']

    merge_result = merge_columns(merge_data_list, merge_data_column)

    y = np.array(wind_farm_overlay_grid['wind_farm_result'], dtype='float32').reshape(-1, 1)
    x = merge_result[merge_data_column].values
    coordinates = list(zip(wind_farm_overlay_grid.centroid.x, wind_farm_overlay_grid.centroid.y))

    gwr_results = gwr(coordinates, y, x)

    if is_gwr_summary:
        gwr_results.summary()

    if is_plot_coefficient:
        cof_data_column = ['cof_wind_farm'] + [f'cof_{col}' for col in merge_data_column]

        gwr_coefficient = pd.DataFrame(gwr_results.params, columns=cof_data_column)
        gwr_filter_t = pd.DataFrame(gwr_results.filter_tvals())

        x_data_geo = merge_result
        x_data_geo = x_data_geo.join(gwr_coefficient)

        plot_coefficient(x_data_geo, cof_data_column, gwr_filter_t)

    print('-=-=-=-=-=-=-=-=-gwr-test-main-function-finished-=-=-=-=-=-=-=-=-')


if __name__ == '__main__':
    plot_factors()
    # gwr_grid(is_gwr_summary=True, is_plot_coefficient=True)

    plt.show()
