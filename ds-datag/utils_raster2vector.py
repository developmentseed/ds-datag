import shapely
import rasterio
from geojson import Feature
import pyproj
from functools import partial
import fiona.crs as fcrs
from shapely.geometry import shape, mapping
from shapely.ops import transform as shpTrans
from shapely.geometry import Polygon


def polygonize_raster(dataset):
    # Read the dataset's valid data mask as a ndarray. Dataset is a rasterio read object open for reading
    mask = dataset.dataset_mask()
    array = dataset.read(1)
    generator = rasterio.features.shapes(source=array.astype(
        'uint8'), mask=mask.astype('uint8'), transform=dataset.transform)
    # Extract feature shapes and values from the array
    features = []
    for geom, value in generator:
        geom = shapely.geometry.shape(geom)
        feature = Feature(geometry=geom, properties={"v": value})
        features.append(feature)
    return features


def polygonize_raster_exterior(dataset):
    # Read the dataset's valid data mask as a ndarray. Dataset is a rasterio read object open for reading
    project = partial(
        pyproj.transform,
        pyproj.Proj(fcrs.from_epsg(3857)),
        pyproj.Proj(4326))
    mask = dataset.dataset_mask()
    array = dataset.read(1)
    generator = rasterio.features.shapes(source=array.astype(
        'uint8'), mask=mask.astype('uint8'), transform=dataset.transform)
    # Extract feature shapes and values from the array
    features = []
    for geom, value in generator:
        geom = shapely.geometry.shape(geom)
        # print(geom.area)
        if geom.area > 1000:
            poly = Polygon(geom.exterior.coords)
            # print(poly.type)
            geom_reporj = shpTrans(project, poly)
            geom_sorted = shapely.ops.transform(lambda x, y: (y, x), geom_reporj)
            feature = Feature(geometry=geom_sorted, properties={"v": value})
            features.append(feature)
    return features

def projectShapes(features, fromCRS, toCRS):
    project = partial(
        pyproj.transform,
        pyproj.Proj(fcrs.from_epsg(fromCRS)),
        pyproj.Proj(toCRS))
    return list(
        {
            'properties': feat['properties'],
            'geometry': mapping(
                shpTrans(
                    project,
                    shape(feat['geometry']))
            )
        } for feat in features
    )
