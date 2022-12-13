from rasterio import plot as raster_plot
import matplotlib.pyplot as plt
from add_widget import add_north, add_scale_bar

from utils.geo_file_path import south_scotland, scotland_power_station, scotland_residence, conservation, wind_farm, \
    temperature, precipitation, population, slope, aspect, land_use, wind_speed, road

STATIC_CRS = 'epsg:27700'

legend_kwds = {'loc': 'lower right',
               'markerscale': 0.3,
               'title_fontsize': 'xx-small',
               'fontsize': 'xx-small'}


def add_legend_column(data):
    arr = [0 if i < 10 else 1 for i in range(data.shape[0])]
    data['legend'] = arr


def replace_legend_texts(legend, new_legend_texts, legend_title=None):
    for ix, eb in enumerate(legend.get_texts()):
        # print(eb.get_text(), "-->", new_legend_text[ix])
        eb.set_text(new_legend_texts[ix])

        legend.set_title(legend_title)


def show_factors():
    fig, ax = plt.subplots(nrows=3, ncols=4, figsize=(12, 7), dpi=100)
    fig.suptitle('Factors')

    axes = ax.flatten()

    ax1 = axes[0]
    ax2 = axes[1]
    ax3 = axes[2]
    ax4 = axes[3]
    ax5 = axes[4]
    ax6 = axes[5]
    ax7 = axes[6]
    ax8 = axes[7]
    ax9 = axes[8]
    ax10 = axes[9]
    ax11 = axes[10]
    ax12 = axes[11]

    add_legend_column(wind_farm)
    ax1.set_title('existing wind farm')
    ax1.set_axis_off()
    wind_farm.to_crs(STATIC_CRS).plot(ax=ax1, column='legend', cmap='Set1', scheme='NaturalBreaks', k=1, legend=True,
                                      legend_kwds=legend_kwds)
    south_scotland.to_crs(STATIC_CRS).plot(ax=ax1, alpha=.2, color='orange')
    replace_legend_texts(ax1.get_legend(), ['existing wind farm'])
    add_north(ax=ax1)
    # add_scale_bar(ax=ax1, lon0=-2, lat0=54.8, length=200, size=0.05)

    add_legend_column(conservation)
    ax2.set_title('conservation')
    ax2.set_axis_off()
    conservation.plot(ax=ax2, column='legend', cmap='Dark2', scheme='NaturalBreaks', k=1, legend=True,
                      legend_kwds=legend_kwds)
    south_scotland.plot(ax=ax2, alpha=.5, color='green')
    replace_legend_texts(ax2.get_legend(), ['conservation'])

    add_legend_column(scotland_residence)
    ax3.set_title('residential area')
    ax3.set_axis_off()
    south_scotland.plot(ax=ax3, color='lightblue')
    scotland_residence.plot(ax=ax3, markersize=1, column='legend', cmap='tab10', scheme='NaturalBreaks', k=1,
                            legend=True, legend_kwds=legend_kwds)
    replace_legend_texts(ax3.get_legend(), ['residential area'])

    add_legend_column(scotland_power_station)
    ax4.set_title('power station')
    ax4.set_axis_off()
    scotland_power_station.plot(ax=ax4, markersize=1, column='legend', cmap='gray', scheme='NaturalBreaks', k=1,
                                legend=True, legend_kwds=legend_kwds, alpha=.6)
    south_scotland.plot(ax=ax4, alpha=.5, color='grey')
    replace_legend_texts(ax4.get_legend(), ['power station'])

    ax5.set_title('temperature')
    ax5.set_axis_off()
    temperature.plot(ax=ax5, column='aveTemp', cmap='Reds', scheme='NaturalBreaks', k=5, legend=True,
                     legend_kwds=legend_kwds)
    replace_legend_texts(ax5.get_legend(), ['5-6', '6-7', '7-8', '8-9', '9-10'], legend_title='temp/°C')

    ax6.set_title('land cover')
    ax6.set_axis_off()
    population.plot(ax=ax6, column='SSP1_2020', cmap='gist_earth', scheme='NaturalBreaks', k=5, legend=True,
                    legend_kwds=legend_kwds)
    replace_legend_texts(ax6.get_legend(),
                         ['Urban', 'Water', 'Woodland\n&Grassland', 'Swamp\n&Bog',
                          'Rock\n&Sediment'])
    raster_plot.show(
        land_use,
        ax=ax6,
        cmap='gist_earth'
    )

    ax7.set_title('slope')
    ax7.set_axis_off()
    population.plot(ax=ax7, column='SSP1_2020', cmap='terrain', scheme='NaturalBreaks', k=5, legend=True,
                    legend_kwds=legend_kwds)
    replace_legend_texts(ax7.get_legend(), ['0-9', '9-18', '18-27', '27-36', '36-45'],
                         legend_title='slope (°)')
    raster_plot.show(
        slope,
        ax=ax7,
        cmap='terrain'
    )

    ax8.set_title('aspect')
    ax8.set_axis_off()
    population.plot(ax=ax8, column='SSP1_2020', cmap='Greys', scheme='NaturalBreaks', k=4, legend=True,
                    legend_kwds=legend_kwds)
    replace_legend_texts(ax8.get_legend(), ['0-90', '90-180', '180-270', '270-260'],
                         legend_title='aspect (°)')
    raster_plot.show(
        aspect,
        ax=ax8,
        cmap='Greys'
    )

    ax9.set_title('population')
    ax9.set_axis_off()
    population.plot(ax=ax9, column='SSP1_2020', cmap='Oranges', scheme='NaturalBreaks', k=5, legend=True,
                    legend_kwds=legend_kwds)
    replace_legend_texts(ax9.get_legend(), ['0.0-0.6', '0.6-2.1', '2.1-4.4', '4.4-7.8', '7.8-13'],
                         legend_title='popu (k)')

    ax10.set_title('wind speed')
    ax10.set_axis_off()
    population.plot(ax=ax10, column='SSP1_2020', cmap='YlGnBu', scheme='NaturalBreaks', k=5, legend=True,
                    legend_kwds=legend_kwds)
    replace_legend_texts(ax10.get_legend(), ['2.2-4.9', '4.9-5.4', '5.4-5.9', '5.9-6.6', '6.6-11'],
                         legend_title='speed (m/s)')
    raster_plot.show(
        wind_speed,
        ax=ax10,
        cmap='YlGnBu'
    )

    ax11.set_title('precipitation')
    ax11.set_axis_off()
    precipitation.plot(ax=ax11, column='prSum', cmap='PuBu', scheme='NaturalBreaks', k=5, legend=True,
                       legend_kwds=legend_kwds)
    replace_legend_texts(ax11.get_legend(), ['0.6-0.9', '0.9-1.2', '1.2-1.6', '1.6-2.0', '2.0-2.8'],
                         legend_title='prec (L)')

    add_legend_column(road)
    ax12.set_title('road')
    ax12.set_axis_off()
    road.to_crs(STATIC_CRS).plot(ax=ax12, linewidth=1, alpha=0.4, column='legend', cmap='gray', scheme='NaturalBreaks',
                                 k=1, legend=True, legend_kwds=legend_kwds)
    south_scotland.to_crs(STATIC_CRS).plot(ax=ax12, alpha=.2, color='grey')
    replace_legend_texts(ax12.get_legend(), ['road'])


if __name__ == '__main__':
    show_factors()

    plt.show()
