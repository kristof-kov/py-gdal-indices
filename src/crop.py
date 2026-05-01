import os
from osgeo import gdal

gdal.UseExceptions()

INPUT_DIR = '../data/S2B_MSIL2A_20210708T094029_N0500_R036_T34UDU_20230203T071138.SAFE/GRANULE/L2A_T34UDU_A022656_20210708T094032/IMG_DATA/R10m'

BAND_3_INPUT = os.path.join(INPUT_DIR, 'T34UDU_20210708T094029_B03_10m.jp2')
BAND_4_INPUT = os.path.join(INPUT_DIR, 'T34UDU_20210708T094029_B04_10m.jp2')
BAND_8_INPUT = os.path.join(INPUT_DIR, 'T34UDU_20210708T094029_B08_10m.jp2')

BAND_3_OUTPUT = '../data/cropped_B03.tif'
BAND_4_OUTPUT = '../data/cropped_B04.tif'
BAND_8_OUTPUT = '../data/cropped_B08.tif'

# bounding box in WGS84
# covers Eger and surroundings
CROP_BOUNDS = (20.1, 47.77, 20.95, 48.15) # (xmin, ymin, xmax, ymax)

def crop_band(input_path: str, output_path: str, bounds: tuple) -> None:
    """Crop a raster to the given WGS84 bounding box and save as GeoTIFF."""
    gdal.Warp(
        output_path,
        input_path,
        outputBounds=bounds,
        outputBoundsSRS='EPSG:4326',
        format='GTiff'
    )
    print(f'  Cropped: {output_path}')
    
def main():
    print('Cropping bands...')
    crop_band(BAND_3_INPUT, BAND_3_OUTPUT, CROP_BOUNDS)
    crop_band(BAND_4_INPUT, BAND_4_OUTPUT, CROP_BOUNDS)
    crop_band(BAND_8_INPUT, BAND_8_OUTPUT, CROP_BOUNDS)
    print('Done.')

if __name__ == '__main__':
    main()