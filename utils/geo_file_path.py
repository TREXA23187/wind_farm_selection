import geopandas as gpd
import rasterio
import os


def file_path_cwd(file_path):
    project_file_name = 'windFarmSelection'

    current_path = os.path.dirname(__file__)
    n = current_path.find(project_file_name)

    root = os.path.join(current_path[:n], project_file_name)
    return os.path.join(root, file_path)


# polyline
road = gpd.read_file(file_path_cwd('resource/Road/south_scotland_road.shp'))
community_council = gpd.read_file(file_path_cwd('resource/Region/shp/south_scotland_community_council.shp'))

# polygon
south_scotland = gpd.read_file(file_path_cwd('resource/Region/shp/south_scotland.shp'))
conservation = gpd.read_file(file_path_cwd('resource/Conservation/south_scotland_conservation.shp'))
temperature = gpd.read_file(file_path_cwd('resource/Temperature/south_scotland_monthly_temperature.shp'))
wind_farm = gpd.read_file(file_path_cwd('resource/WindFarm/south_scotland_wind_farm.shp'))
precipitation = gpd.read_file(file_path_cwd('resource/Precipitation/south_scotland_precipitation.shp'))
population = gpd.read_file(file_path_cwd('resource/Population/south_scotland_population.shp'))
landscape = gpd.read_file(file_path_cwd('resource/Landscape/south_scotland_landscape.shp'))

# point
scotland_power_station = gpd.read_file(file_path_cwd('resource/EnergySupply/south_scotland_energy_station.shp'))
scotland_residence = gpd.read_file(file_path_cwd('resource/Residence/south_scotland_residence.shp'))

# raster
elevation = rasterio.open(file_path_cwd('resource/Elevation/south_scotland_elevation.tif'))
slope = rasterio.open(file_path_cwd('resource/Elevation/slope.tif'))
aspect = rasterio.open(file_path_cwd('resource/Elevation/aspect.tif'))
land_use = rasterio.open(file_path_cwd('resource/LandUse/south_scotland_land_use.tif'))
wind_speed = rasterio.open(file_path_cwd('resource/WindSpeed/south_scotland_wind_speed.tif'))

if __name__ == '__main__':
    path = os.path.dirname(__file__)
