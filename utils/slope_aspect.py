from osgeo import gdal


def callback(process_type):
    print(f'--- {process_type} processing finished ---')


def process(input_path, output_path, process_type, cb=callback):
    gdal.DEMProcessing(output_path, input_path, process_type, callback=cb(process_type))


if __name__ == '__main__':
    data = 'resource/Elevation/south_scotland_elevation.tif'
    slope_path = 'resource/Elevation/slope.tif'
    aspect_path = 'resource/Elevation/aspect.tif'

    # process(data, slope_path, 'slope')
