## Wind Farm Selection in Southern Scotland

wind_farm_resource:
~~https://pan.baidu.com/s/1lChEqwGumxRPfZfz93iECA?pwd=wind~~
https://pan.baidu.com/s/1orss9lbNJsvjF3wHQlHRew?pwd=wind

本项目所需用到的Southern Scatland的各项数据，下载后放到与`main.py`同级目录下。

### main.py

```python
from utils.show_factor import show_factors
from utils.model_ward_test import model_ward,plot_ward_factors

import matplotlib.pyplot as plt

show_factors()

plot_ward_factors()
model_ward(is_summary=True, is_plot_coefficient=True)

plt.show()
```

### utils

#### geo_file_path.py

`file_path_cwd()`是通过项目名称**'windFarmSelection'**将所需的数据资源文件进行拼接返回的，所以需要尽量保证项目文件名一致，或者保持同步更改。

```python
def file_path_cwd(file_path):
    project_file_name = 'windFarmSelection'

    current_path = os.path.dirname(__file__)
    n = current_path.find(project_file_name)

    root = os.path.join(current_path[:n], project_file_name)
    return os.path.join(root, file_path)
```

用来存储所有可能用到的shp和tif文件通过`gpd.read_file`和`rasterio.open`提前读取，因此项目中其他所需数据导入部分全部将引用该文件。

```python
from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm,temperature, precipitation, population, road, community_council, landscape
```

#### show_factor.py

展示 existing wind farm 以及可能影响其分布的11个要素。

```python
    add_legend_column(wind_farm)  # add a column as legend
    ax1.set_title('existing wind farm')  # set title
    ax1.set_axis_off()  # not show axis
    wind_farm.to_crs(STATIC_CRS).plot(ax=ax1, column='legend', cmap='Set1', scheme='NaturalBreaks', k=1, legend=True,legend_kwds=legend_kwds)  # plot with legend
    south_scotland.to_crs(STATIC_CRS).plot(ax=ax1, alpha=.2, color='orange')  # plot south scotland as basemap
    replace_legend_texts(ax1.get_legend(), ['existing wind farm'])  # set legend text
    add_north(ax=ax1)  # add compass
```

#### model_ward_xx.py

包含以下七种模型并对比其结果。

- `modeil_ward_test.py`作为测试时快速的预览`plot`后的图像，不包含`slope`、`wind_speed`、`land_use`，该三种数据由其tif文件转成shp文件得到，文件转成`Dataframe`后行列的数据较多，避免每次运行程序都执行读取这些数据，因此这三个shp文件将不在`geo_file_path.py`中统一读取。
- `modeil_ward_release.py`则包含最终出图时所有的数据，得到模型结果与结果图像需要一定时间。

| Model          | Describe                                                     |
| -------------- | ------------------------------------------------------------ |
| spreg.OLS      | Ordinary least squares with results and diagnostics.         |
| spreg.ML_Lag   | ML estimation of the spatial lag model with all results and diagnostics. |
| spreg.ML_Error | ML estimation of the spatial error model with all results and diagnostics. |
| spreg.GM_Lag   | Spatial two stage least squares (S2SLS) with results and diagnostics. |
| spreg.GM_Error | GMM method for a spatial error model, with results and diagnostics. |
| mgwr.gwr.GWR   | Geographically weighted regression.                          |
| mgwr.gwr.MGWR  | Multiscale GWR estimation and inference.                     |

##### plot_ward_factors()

根据Southern Scotland的分区，将以上12种要素分别计算其在对应分区内的值，计算规则如下：

- 点要素：计算每个分区内包含的点个数
- 线要素：计算每个分区内包含的线段长度
- 面要素：计算每个分区内包含的区域的面积

最终得到12个分别包含有每个要素合并到分区数据，通过`plot_ward_factors()`进行展示。

##### model_ward(is_summary=True, is_plot_coefficient=True)

- `is_summary=True`: 是否输出对应模型的诊断结果，其中不同模型对应的输出summary的方式如下：

  - ols、ml_lag、ml_error、gm_lag、gm_error:

    `print(result.summary)`

  - gwr、mgwr: `result.summary()`

- `is_plot_coefficient=True` : 是否展示诊断结果对应coefficient的图

#### add_widget.py

在对应区域添加指北针`add_north()`和比例尺`add_scale_bar()`

#### raster_to_vector.py

栅格转矢量

#### slope_aspect.py

根据高程DEM.tif数据得到对应`slope`坡度和`aspect`坡向。

### diagnostics summary

各模型的诊断结果各指标的解读和模型间的相互对比。（未完成）
