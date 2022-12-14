import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from pyproj import CRS

from mgwr.gwr import GWR, MGWR
from mgwr.sel_bw import Sel_BW
from spreg.ols import OLS
from spreg.ml_lag import ML_Lag
from spreg.ml_error import ML_Error
from spreg import GM_Lag
from spreg import GM_Error
from pysal.lib import weights

from spreg.diagnostics import likratiotest

from matplotlib import colors
from matplotlib import cm

from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm, \
    temperature, precipitation, population, road, community_council, landscape
from add_widget import add_north, add_scale_bar

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False
# pd.set_option('display.max_rows', None)

CRS_4326 = CRS('epsg:4326')
STATIC_CRS = CRS('epsg:27700')

GRID_NUM = 32

wind_speed = gpd.read_file('../resource/RasterToVector/wind_speed_shp.shp')
land_use = gpd.read_file('../resource/RasterToVector/land_use_shp.shp')

# aspect = gpd.read_file('../resource/RasterToVector/aspect_shp.shp')
slope = gpd.read_file('../resource/RasterToVector/slope_shp.shp')


def generate_ward():
    return community_council.reset_index()


def get_ward_contain_point(name, right_df):
    contain_grid = generate_ward()

    result_column = f'{name}_result'
    residence_join = gpd.sjoin(left_df=contain_grid, right_df=right_df.to_crs(STATIC_CRS), op='contains').groupby(
        'index')[
        'id'].count().to_frame().reset_index()

    residence_join.columns = ['index', result_column]

    contain_grid = pd.merge(contain_grid, residence_join, on='index', how='outer')
    contain_grid[result_column] = contain_grid[result_column].fillna(0)

    return contain_grid


def get_ward_overlay_area(name, df2, value_column=None, ):
    overlay_grid = generate_ward()

    result_column = f'{name}_result'

    overlay_result = gpd.overlay(df1=overlay_grid, df2=df2.to_crs(STATIC_CRS), how='intersection')
    overlay_result[result_column] = overlay_result[value_column] if value_column else overlay_result.area / 10000
    overlay_result = pd.merge(overlay_grid, overlay_result, on='index', how='left')

    arr = [0 for _ in range(286)]

    for i in range(overlay_result.shape[0]):
        index = overlay_result.loc[i, 'index']
        value = overlay_result.loc[i, result_column]
        arr[index] += value

    overlay_grid[result_column] = arr
    overlay_grid[result_column] = overlay_grid[result_column].fillna(0.0)
    overlay_grid.rename(columns={'geometry_x': 'geometry'}, inplace=True)

    return overlay_grid


def get_ward_overlay_line(name, df2):
    overlay_line_grid = generate_ward()
    result_column = f'{name}_result'
    overlay_line_result = gpd.overlay(df1=overlay_line_grid, df2=df2.to_crs(STATIC_CRS), keep_geom_type=False)
    overlay_line_result[result_column] = overlay_line_result.length
    overlay_line_result = pd.merge(overlay_line_grid, overlay_line_result, on='index', how='left')

    array = [0 for _ in range(286)]

    for i in range(overlay_line_result.shape[0]):
        index = overlay_line_result.loc[i, 'index']
        value = overlay_line_result.loc[i, result_column]
        array[index] += value

    overlay_line_grid[result_column] = array
    overlay_line_grid[result_column] = overlay_line_grid[result_column].fillna(0.0)

    return overlay_line_grid


def plot_axis_grid(name, ax, display_grid=None):
    ax.set_title(name)
    ax.set_axis_off()

    # normalization
    result = display_grid[f'{name}_result']
    display_grid[f'{name}_result_normalised'] = (result - result.min(axis=0)) / (
            result.max(axis=0) - result.min(axis=0))
    if display_grid is not None:
        display_grid.plot(ax=ax, column=f'{name}_result_normalised', cmap='YlOrRd', edgecolor='Black', legend=True,
                          linewidth=.5)


def plot_ward_factors():
    fig, axis = plt.subplots(nrows=3, ncols=4, figsize=(12, 7), dpi=100)
    fig.suptitle('Ward Factors Input')

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

    residence_grid = get_ward_contain_point('residence', scotland_residence)

    scotland_power_station['id'] = scotland_power_station.index
    power_station_grid = get_ward_contain_point('power_station', scotland_power_station)

    conservation_overlay_grid = get_ward_overlay_area('conservation', conservation)
    wind_farm_overlay_grid = get_ward_overlay_area('wind_farm', wind_farm)
    temperature_overlay_grid = get_ward_overlay_area('temperature', temperature, value_column='aveTemp')
    precipitation_overlay_grid = get_ward_overlay_area('precipitation', precipitation, value_column='prSum')
    population_overlay_grid = get_ward_overlay_area('population', population, value_column='SSP1_2020')
    landscape_grid = get_ward_overlay_area('landscape', landscape)

    road_overlay_grid = get_ward_overlay_line('road', road)
    community_council_grid = get_ward_overlay_line('community_council', community_council)

    wind_speed_grid = get_ward_overlay_area('wind_speed', wind_speed[wind_speed['DN'] > 6], value_column='DN')
    land_use_grid = get_ward_overlay_area('land_use', land_use[land_use['DN'] <= 10], value_column='DN')
    slope_grid = get_ward_overlay_area('slope', slope[slope['DN'] < 15], value_column='DN')

    # plot
    plot_axis_grid('wind_farm', ax1, wind_farm_overlay_grid)
    add_north(ax=ax1)
    plot_axis_grid('residence', ax2, residence_grid)
    plot_axis_grid('power_station', ax3, power_station_grid)
    plot_axis_grid('conservation', ax4, conservation_overlay_grid)
    plot_axis_grid('temperature', ax5, temperature_overlay_grid)
    plot_axis_grid('precipitation', ax6, precipitation_overlay_grid)
    plot_axis_grid('population', ax7, population_overlay_grid)
    plot_axis_grid('road', ax8, road_overlay_grid)
    plot_axis_grid('slope', ax9, slope_grid)
    plot_axis_grid('landscape', ax10, landscape_grid)
    plot_axis_grid('wind_speed', ax11, wind_speed_grid)
    plot_axis_grid('land_use', ax12, land_use_grid)
    add_scale_bar(ax=ax12, lon0=370000, lat0=535000)

    # norm = colors.Normalize(vmin=0, vmax=1)
    # fig.colorbar(cm.ScalarMappable(norm=norm, cmap='YlOrRd'), ax=axis, orientation='horizontal', shrink=.7, aspect=30,
    #              pad=.1)


def plot_coefficient(geo_data, cof_data_column, gwr_filter_t):
    fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(12, 7))
    axes = ax.flatten()
    fig.suptitle('Ward Factors Coefficient Output')

    for i in range(0, len(cof_data_column)):
        ax = axes[i]
        ax.set_title(cof_data_column[i])
        geo_data.plot(ax=ax, column=cof_data_column[i], edgecolor='white', cmap='Blues', vmin=-1, vmax=1,
                      legend=True,
                      # scheme='User_Defined',
                      # classification_kwds=dict(bins=[-1, -0.5, 0, 0.5, 1]),
                      # legend_kwds=legend_kwds
                      )

        if (gwr_filter_t[i] == 0).any():
            geo_data[gwr_filter_t[i] == 0].plot(color='lightgrey', ax=ax, edgecolor='white')

    for i in range(0, len(axes)):
        ax = axes[i]
        ax.set_axis_off()

    add_north(ax=axes[0])
    add_scale_bar(ax=axes[-1], lon0=370000, lat0=535000)


def ols(y, x, w, name_y, name_x):
    ols_result = OLS(y, x, w, spat_diag=True, moran=True, name_y=name_y, name_x=name_x, name_ds=name_y,
                     name_w='queen')

    return ols_result


def ml_lag(y, x, w, name_y, name_x):
    ml_lag_result = ML_Lag(y, x, w, name_y=name_y, name_x=name_x, name_ds=name_y, name_w='queen')

    return ml_lag_result


def ml_error(y, x, w, name_y, name_x):
    ml_error_result = ML_Error(y, x, w, name_y=name_y, name_x=name_x, name_ds=name_y, name_w='queen')

    return ml_error_result


def gwr(y, x, coordinates):
    g_x = (x - x.mean(axis=0)) / x.std(axis=0)
    g_y = (y - y.mean(axis=0)) / y.std(axis=0)
    gwr_selector = Sel_BW(coordinates, y, x)
    # gwr_bw = gwr_selector.search(search_method='golden_section', criterion='AIC') - 0.633
    # gwr_bw = gwr_selector.search(search_method='scipy', criterion='AIC') - 0.633
    gwr_bw = gwr_selector.search(search_method='golden_section', criterion='AIC')
    # print('best gwr：', gwr_bw)

    gwr_results = GWR(coordinates, g_y, g_x, bw=gwr_bw, fixed=False, kernel='gaussian', constant=True,
                      spherical=True).fit()

    return gwr_results


def mgwr(y, x, coordinates):
    g_x = (x - x.mean(axis=0)) / x.std(axis=0)
    g_y = (y - y.mean(axis=0)) / y.std(axis=0)

    mgwr_selector = Sel_BW(coordinates, g_y, g_x, multi=True)
    mgwr_bw = mgwr_selector.search()
    mgwr_results = MGWR(coordinates, g_y, g_x, selector=mgwr_selector).fit()  # 0.823

    return mgwr_results


def gm_lag(y, x, w, name_y, name_x):
    gm_lag_result = GM_Lag(y, x, w=w, w_lags=2, robust='white', name_y=name_y, name_x=name_x, name_ds=name_y,
                           name_w='queen')

    return gm_lag_result


def gm_error(y, x, w, name_y, name_x):
    gm_error_result = GM_Error(y, x, w=w, name_y=name_y, name_x=name_x, name_ds=name_y, name_w='queen')

    return gm_error_result


def merge_columns(merge_data_list, merge_data_column, merge_result=generate_ward()):
    for i in range(len(merge_data_list)):
        col = merge_data_column[i]
        merge_result = pd.merge(merge_result, merge_data_list[i][['index', col]], on='index')

    return merge_result


def model_ward(is_gwr_summary=False, is_plot_coefficient=False, method_list=['gwr']):
    wind_farm_overlay_grid = get_ward_overlay_area('wind_farm', wind_farm)

    residence_grid = get_ward_contain_point('residence', scotland_residence)
    scotland_power_station['id'] = scotland_power_station.index
    power_station_grid = get_ward_contain_point('power_station', scotland_power_station)
    conservation_overlay_grid = get_ward_overlay_area('conservation', conservation)
    temperature_overlay_grid = get_ward_overlay_area('temperature', temperature, value_column='aveTemp')
    precipitation_overlay_grid = get_ward_overlay_area('precipitation', precipitation, value_column='prSum')
    population_overlay_grid = get_ward_overlay_area('population', population, value_column='SSP1_2020')
    road_overlay_grid = get_ward_overlay_line('road', road)
    slope_grid = get_ward_overlay_area('slope', slope[slope['DN'] < 15], value_column='DN')
    landscape_grid = get_ward_overlay_area('landscape', landscape)
    wind_speed_grid = get_ward_overlay_area('wind_speed', wind_speed, value_column='DN')
    land_use_grid = get_ward_overlay_area('land_use', land_use[land_use['DN'] <= 10], value_column='DN')

    merge_data_list = [residence_grid, power_station_grid, conservation_overlay_grid, temperature_overlay_grid,
                       precipitation_overlay_grid, population_overlay_grid, road_overlay_grid,
                       slope_grid, landscape_grid, wind_speed_grid, land_use_grid]
    merge_data_column = ['residence_result', 'power_station_result', 'conservation_result', 'temperature_result',
                         'precipitation_result', 'population_result', 'road_result',
                         'slope_result', 'landscape_result', 'wind_speed_result', 'land_use_result']

    merge_result = merge_columns(merge_data_list, merge_data_column)

    y = np.array(wind_farm_overlay_grid['wind_farm_result'], dtype='float32').reshape(-1, 1)
    x = merge_result[merge_data_column].values
    coordinates = list(zip(wind_farm_overlay_grid.centroid.x, wind_farm_overlay_grid.centroid.y))
    w_queen = weights.Queen.from_dataframe(community_council)

    # ols_result = ols(y, x, w_queen, name_y='wind_farm', name_x=merge_data_column)
    # print(ols_result.summary)

    # gwr_result = gwr(y, x, coordinates)
    # gwr_result.summary()

    mgwr_result = mgwr(y, x, coordinates)
    mgwr_result.summary()

    # ml_lag_result = ml_lag(y, x, w_queen, name_y='wind_farm', name_x=merge_data_column)
    # print(ml_lag_result.summary)
    #
    # ml_error_result = ml_error(y, x, w_queen, name_y='wind_farm', name_x=merge_data_column)
    # print(ml_error_result.summary)

    # gm_lag_result = gm_lag(y, x, w_queen, name_y='wind_farm', name_x=merge_data_column)
    # print(gm_lag_result.summary)
    #
    # gm_error_result = gm_error(y, x, w_queen, name_y='wind_farm', name_x=merge_data_column)
    # print(gm_error_result.summary)

    # if is_gwr_summary:
    #     method_results.summary()
    #
    if is_plot_coefficient:
        cof_data_column = ['cof_wind_farm'] + [f'cof_{col}' for col in merge_data_column]

        gwr_coefficient = pd.DataFrame(mgwr_result.params, columns=cof_data_column)
        gwr_filter_t = pd.DataFrame(mgwr_result.filter_tvals())

        x_data_geo = merge_result

        x_data_geo = x_data_geo.join(gwr_coefficient)

        plot_coefficient(x_data_geo, cof_data_column, gwr_filter_t)

    print('-=-=-=-=-=-=-=-=-gwr-ward-main-function-finished-=-=-=-=-=-=-=-=-')


if __name__ == '__main__':
    plot_ward_factors()
    model_ward(is_gwr_summary=True, is_plot_coefficient=True, method_list=[])

    plt.show()
