import os
import rasterio
from rasterio.features import shapes
import geopandas as gpd
from shapely.geometry import shape
from fiona.crs import from_epsg

def process_tif_files(tif_folder_path, output_shapefile_folder, region_shapefile_path):
    intersected_tifs = []
    non_intersected_tifs = []

    # Read the region shapefile
    region_gdf = gpd.read_file(region_shapefile_path)

    # Output CRS
    output_crs = region_gdf.crs

    for tif_file in os.listdir(tif_folder_path):
        if tif_file.endswith(".tif"):
            # Construct the full path to the TIFF file
            tif_path = os.path.join(tif_folder_path, tif_file)

            # Open the Sentinel-2 TIFF file
            with rasterio.open(tif_path) as src:
                # Read the image and transform it to a binary mask (1 for data, 0 for nodata)
                image = src.read(1)
                mask = (image > 0).astype('uint8')

                # Get the transform and profile of the raster
                transform = src.transform

            # Generate vector shapes from the binary mask
            vector_shapes = list(shapes(mask, transform=transform))

            # Convert vector shapes to GeoDataFrame
            gdf = gpd.GeoDataFrame(geometry=[shape(geom) for geom, value in vector_shapes], crs=output_crs)

            # Construct the output shapefile path based on the TIFF file name
            output_shapefile_path = os.path.join(output_shapefile_folder, os.path.splitext(tif_file)[0] + "_border.shp")

            # Save the GeoDataFrame to a shapefile
            gdf.to_file(output_shapefile_path)

            # Check for intersection with the region shapefile
            if gdf.intersects(region_gdf.unary_union).any():
                intersected_tifs.append(tif_file)
            else:
                non_intersected_tifs.append(tif_file)

            print(f"Vector layer saved to: {output_shapefile_path}")

    print("\nTIFF files with intersection:", intersected_tifs)
    print("\nTIFF files with no intersection:", non_intersected_tifs)

# Example usage:
tif_folder_path = "C:\\Users\\Cengiz\\Desktop\\raster_filter"
output_shapefile_folder = "C:\\Users\\Cengiz\\Desktop\\raster_filter\\shps"
region_shapefile_path = "C:\\Users\\Cengiz\\Desktop\\raster_filter\\region.shp"

process_tif_files(tif_folder_path, output_shapefile_folder, region_shapefile_path)
