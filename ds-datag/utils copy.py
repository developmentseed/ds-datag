import os
from smart_open import open
import json
from geojson import FeatureCollection
from shapely.geometry import shape
import requests
import rioxarray


def save_featurecollection(features, path_file):
    with open(path_file, 'w') as f:
        json.dump(FeatureCollection(features), f)
        print(f"Save {path_file}")


def get_dataArray(name, url):
    dataArray = None
    try:
        dataArray = rioxarray.open_rasterio(url, decode_coords="all")
    except:
        print(f'No tile resource for {name}')
    return dataArray


def read_geojson(input_file: str):
    """Read a geojson file and return a list of features.

    Args:
        input_file (str): Location on geojson file

    Returns:
        list: list fo features
    """
    feature_collection = []
    with open(input_file, "r", encoding="utf8") as f:
        feature_collection = json.load(f)["features"]
    return feature_collection


def write_geojson(output_file: str, list_features: list):
    """Write geojson files.

    Args:
        output_file (str): Location of ouput file
        list_features (list): List of features
    """
    with open(output_file, "w") as f:
        json.dump(FeatureCollection(list_features), f)


def check_geometry(feature: dict):
    """Verify if geometry is valid.

    Args:
        feat (dict): Feature

    Returns:
        Bool: Return false or true acoording to the geometry
    """
    try:
        geom_shape = shape(feature["geometry"])
        return geom_shape.is_valid
    except Exception:
        return False


def create_folder(tiles_folder):
    """Create folder in local in case is needed."""
    if tiles_folder[:5] not in ["s3://", "gs://"]:
        os.makedirs(tiles_folder, exist_ok=True)


def fetch_tile(tile, url):
    """Fetch a tiles"""
    # print(type(tile))
    tile = [str(t) for t in tile]
    tile_str = "-".join(tile)
    tile_file = f"data/{tile_str}.tif"

    if not os.path.isfile(tile_file):
        try:
            r = requests.get(url, timeout=200000)
            if r.status_code == 200:
                with open(tile_file, "wb") as f:
                    f.write(r.content)
            else:
                tile_file = None
        except:
            print(f'No tile resource for {tile_file}')
            tile_file = None

    return tile_file
