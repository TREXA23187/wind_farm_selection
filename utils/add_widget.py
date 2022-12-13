import matplotlib.patches as mpatches
from shapely.geometry import Point
import geopandas as gpd


def distance(p1, p2, crs='epsg:27700'):
    pnt1 = Point(p1[0], p1[1])
    pnt2 = Point(p2[0], p2[1])
    points_df = gpd.GeoDataFrame({'geometry': [pnt1, pnt2]}, crs=crs)
    points_df2 = points_df.shift()

    distance_df = points_df.distance(points_df2)
    distance_df = distance_df.reset_index()
    distance_df.columns = ['index', 'distance']
    distance_df.index = ['d1', 'd2']

    return distance_df.loc['d2', 'distance']


def add_north(ax, label_size=10, loc_x=0.1, loc_y=0.85, width=0.1, height=0.2, pad=0.14):
    """
    画一个指北针带'N'文字注释
    :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
    :param label_size: 显示'N'文字的大小
    :param loc_x: 以文字下部为中心的占整个ax横向比例
    :param loc_y: 以文字下部为中心的占整个ax纵向比例
    :param width: 指北针占ax比例宽度
    :param height: 指北针占ax比例高度
    :param pad: 文字符号占ax比例间隙
    :return: None
    """
    minx, maxx = ax.get_xlim()
    miny, maxy = ax.get_ylim()
    ylen = maxy - miny
    xlen = maxx - minx
    left = [minx + xlen * (loc_x - width * .5), miny + ylen * (loc_y - pad)]
    right = [minx + xlen * (loc_x + width * .5), miny + ylen * (loc_y - pad)]
    top = [minx + xlen * loc_x, miny + ylen * (loc_y - pad + height)]
    center = [minx + xlen * loc_x, left[1] + (top[1] - left[1]) * .4]
    triangle = mpatches.Polygon([left, top, right, center], color='k')
    ax.text(s='N',
            x=minx + xlen * loc_x,
            y=miny + ylen * (loc_y - pad + height),
            fontsize=label_size,
            horizontalalignment='center',
            verticalalignment='bottom')
    ax.add_patch(triangle)


def add_scale_bar(ax, lon0, lat0, length=50000, size=5000):
    """
    ax: 坐标轴
    lon0: 经度
    lat0: 纬度
    length: 长度
    size: 控制粗细和距离的
    """

    ax.hlines(y=lat0, xmin=lon0, xmax=lon0 + length, colors="black", ls="-", lw=1, label=f'{length} km')
    ax.vlines(x=lon0, ymin=lat0, ymax=lat0 + size, colors="black", ls="-", lw=1)
    ax.vlines(x=lon0 + length, ymin=lat0, ymax=lat0 + size, colors="black", ls="-", lw=1)

    scale_distance = distance([lon0, lat0], [lon0 + length, lat0])

    ax.text(lon0 + length / 2, lat0 + 2 * size, f'{int(scale_distance / 1000)} km', horizontalalignment='center')
