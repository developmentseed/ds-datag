import os
from smart_open import open
import json
from geojson import FeatureCollection
from shapely.geometry import shape


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
