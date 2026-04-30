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
     
    dataset_b3 = gdal.Open(BAND_3_PATH)
    dataset_b4 = gdal.Open(BAND_4_PATH)
    dataset_b8 = gdal.Open(BAND_8_PATH)

    if dataset_b3 is None or dataset_b4 is None or dataset_b8 is None:
        print("Error: Could not open datasets with GDAL")
        return
    
    geotransform = dataset_b8.GetGeoTransform()
    projection = dataset_b8.GetProjection()
    cols = dataset_b8.RasterXSize
    rows = dataset_b8.RasterYSize

    array_green = dataset_b3.GetRasterBand(1).ReadAsArray().astype(np.float32)
    array_red = dataset_b4.GetRasterBand(1).ReadAsArray().astype(np.float32)
    array_nir = dataset_b8.GetRasterBand(1).ReadAsArray().astype(np.float32)

    dataset_b3 = None
    dataset_b4 = None
    dataset_b8 = None

    # Index calculation (NDVI and NDWI)
    print('Calculating indices...')
    denominator_ndvi = array_nir + array_red
    ndvi = np.where(denominator_ndvi == 0, 0.0, (array_nir - array_red) / denominator_ndvi).astype(np.float32)
    
    denominator_ndwi = array_green + array_nir
    ndwi = np.where(denominator_ndwi == 0, 0.0, (array_green - array_nir) / denominator_ndwi).astype(np.float32)
    
    print(f'  NDVI  min={ndvi.min():.4f}  max={ndvi.max():.4f}  mean={ndvi.mean():.4f}')
    print(f'  NDWI  min={ndwi.min():.4f}  max={ndwi.max():.4f}  mean={ndwi.mean():.4f}')

    # Saving results to GeoTIFF
    print('Saving output files...')
    # TODO: write arrays to .tif files with spatial references

if __name__ == '__main__':
    main()
