# imports
import geopandas as gpd
import matplotlib.pyplot as plt
from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm, \
    temperature, precipitation, population, slope, aspect, land_use, wind_speed, road

STATIC_CRS = 'epsg:27700'

legend_kwd = {'loc': 'lower right',
              'markerscale': 0.3,
              'title_fontsize': 'small',
              'fontsize': 'xx-small'}

fig_base = plt.figure(figsize=(6, 6), dpi=100)
ax = fig_base.add_subplot(111)
ax.set_axis_off()

arr = [0 if i < 10 else 1 for i in range(wind_farm.shape[0])]
wind_farm['legend'] = arr
print(wind_farm.columns)

wind_farm.to_crs(STATIC_CRS).plot(ax=ax, column='legend', cmap='Set1', scheme='NaturalBreaks', k=1, legend=True,
                                  legend_kwds=legend_kwd)
# temperature.plot(ax=ax, column='aveTemp', cmap='Reds', scheme='NaturalBreaks', k=1, legend=True,
#                  legend_kwds=legend_kwd)
south_scotland.to_crs(STATIC_CRS).plot(ax=ax, alpha=.2, color='orange')

leg = ax.get_legend()
# leg.set_title("legend")

new_legtxt = ["wind farm"]
for ix, eb in enumerate(leg.get_texts()):
    print(eb.get_text(), "-->", new_legtxt[ix])
    eb.set_text(new_legtxt[ix])
plt.show()
