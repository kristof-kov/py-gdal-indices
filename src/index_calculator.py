import os
import numpy as np
from osgeo import gdal

# Configuration and file paths
DATA_DIR = '../data/S2B_MSIL2A_20210708T094029_N0500_R036_T34UDU_20230203T071138.SAFE/GRANULE/L2A_T34UDU_A022656_20210708T094032/IMG_DATA/R10m'

BAND_3_PATH = os.path.join(DATA_DIR, 'T34UDU_20210708T094029_B03_10m.jp2') # green
BAND_4_PATH = os.path.join(DATA_DIR, 'T34UDU_20210708T094029_B04_10m.jp2') # red
BAND_8_PATH = os.path.join(DATA_DIR, 'T34UDU_20210708T094029_B08_10m.jp2') # NIR

OUTPUT_NDVI_PATH = '../data/eger_ndvi_2021.tif'
OUTPUT_NDWI_PATH = '../data/eger_ndwi_2021.tif'

def main():
    print('Starting Sentinel-2 Index Calculation...')

    # Check if files exist before processing
    if not os.path.exists(BAND_3_PATH) or not os.path.exists(BAND_4_PATH) or not os.path.exists(BAND_8_PATH):
        print(f'Error: Could not find source files')
        return
    
    # Readig data with GDAL
    print('Loading satellite bands...')
    # TODO: open datasets and read as NumPy arrays

    # Index calculation (NDVI and NDWI)
    print('Calculating indices...')
    # TODO: implement math formulas

    # Saving results to GeoTIFF
    print('Saving output files...')
    # TODO: write arrays to .tif files with spatial references

if __name__ == '__main__':
    main()
