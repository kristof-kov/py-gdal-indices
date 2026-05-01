import os
import numpy as np
from osgeo import gdal

# Configuration and file paths
gdal.UseExceptions()

DATA_DIR = '../data/S2B_MSIL2A_20210708T094029_N0500_R036_T34UDU_20230203T071138.SAFE/GRANULE/L2A_T34UDU_A022656_20210708T094032/IMG_DATA/R10m'

BAND_3_PATH = os.path.join(DATA_DIR, 'T34UDU_20210708T094029_B03_10m.jp2') # green
BAND_4_PATH = os.path.join(DATA_DIR, 'T34UDU_20210708T094029_B04_10m.jp2') # red
BAND_8_PATH = os.path.join(DATA_DIR, 'T34UDU_20210708T094029_B08_10m.jp2') # NIR

OUTPUT_NDVI_PATH = '../data/eger_ndvi_2021.tif'
OUTPUT_NDWI_PATH = '../data/eger_ndwi_2021.tif'

def load_band(path: str) -> np.ndarray:
    """Open a single-band raster file and return its data as a float32 array."""
    dataset = gdal.Open(path)
    if dataset is None:
        raise IOError(f'GDAL could not open file: {path}')
    array = dataset.GetRasterBand(1).ReadAsArray().astype(np.float32)
    dataset = None
    return array

def get_raster_metadata(path: str) -> tuple:
    """Extract spatial metadata (geotransform, projection, dimensions) from a raster file."""
    dataset = gdal.Open(path)
    if dataset is None:
        raise IOError(f'GDAL could not open file: {path}')
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize
    dataset = None
    return geotransform, projection, cols, rows

def save_geotiff(array: np.ndarray, output_path: str,
                 geotransform: tuple, projection: str,
                 cols: int, rows: int) -> None:
    """Write a 2D float32 array to a single-band GeoTIFF with spatial reference."""
    driver = gdal.GetDriverByName('GTiff')
    out_dataset = driver.Create(output_path, cols, rows, 1, gdal.GDT_Float32)
    out_dataset.SetGeoTransform(geotransform)
    out_dataset.SetProjection(projection)
    out_dataset.GetRasterBand(1).WriteArray(array)
    out_dataset.GetRasterBand(1).FlushCache()
    out_dataset = None
    print(f'  Saved: {output_path}')
    

def main():
    print('Starting Sentinel-2 Index Calculation...')

    # Check if files exist before processing
    if not os.path.exists(BAND_3_PATH) or not os.path.exists(BAND_4_PATH) or not os.path.exists(BAND_8_PATH):
        print(f'Error: Could not find source files')
        return
    
    # Readig data with GDAL
    print('Loading satellite bands...')
    array_green = load_band(BAND_3_PATH)
    array_red = load_band(BAND_4_PATH)
    array_nir = load_band(BAND_8_PATH)
    geotransform, projection, cols, rows = get_raster_metadata(BAND_8_PATH)

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
    save_geotiff(ndvi, OUTPUT_NDVI_PATH, geotransform, projection, cols, rows)
    save_geotiff(ndwi, OUTPUT_NDWI_PATH, geotransform, projection, cols, rows)

if __name__ == '__main__':
    main()
