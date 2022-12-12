import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world['gdp_per_cap'] = world.gdp_md_est / world.pop_est
num_classes = 4  # quartile scheme has 4 classes
# You can use values derived from your preferred classification scheme here
num_qtiles = [0, .25, .5, .75, 1.]  # class boundaries for quartiles
# Here is the categorical data to append to the dataframe
# They are also used as legend's label texts
qlabels = ["1st quartile", "2nd quartile", "3rd quartile", "4th quartile"]  # matching categorical data/labels
# Conditions
# len(num_qtiles)-1 == num_classes
# len(qlabels) == num_classes
# Create a new column for the categorical data mentioned above
world['gdp_quartile'] = pd.qcut(world['gdp_per_cap'], num_qtiles, labels=qlabels)
# Plotting the categorical data for checking
ax1 = world['gdp_quartile'].value_counts().plot(figsize=(5, 4), kind='bar', xlabel='Quartile_Classes',
                                                ylabel='Countries', rot=45, legend=True)

fig, ax = plt.subplots(figsize=(9, 4))
# num_classes = 4 # already defined
# color_steps = plt.colormaps['Reds']._resample(num_classes)   #For older version
color_steps = plt.colormaps['Reds']  # Current version of matplotlib
# This plots choropleth map using categorical data as the theme
world.plot(column='gdp_quartile', cmap=color_steps,
           legend=True,
           legend_kwds={'loc': 'lower left',
                        'bbox_to_anchor': (0, .2),
                        'markerscale': 1.29,
                        'title_fontsize': 'medium',
                        'fontsize': 'small'},
           ax=ax)
leg1 = ax.get_legend()
leg1.set_title("GDP per capita")
ax.title.set_text("World Map: GDP per Capita")

new_legtxt = ["low", "mid", "high", "v.high"]
for ix, eb in enumerate(leg1.get_texts()):
    print(eb.get_text(), "-->", new_legtxt[ix])
    eb.set_text(new_legtxt[ix])
plt.show()
