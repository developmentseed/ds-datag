import shapely
import rasterio
from geojson import Feature
import pyproj
from functools import partial
import fiona.crs as fcrs
from shapely.geometry import shape, mapping
from shapely.ops import transform as shpTrans
from shapely.geometry import Polygon, LineString
from shapely.ops import unary_union
import itertools
from shapely import ops


def dataset2geom(dataset):
    mask = dataset.dataset_mask()
    array = dataset.read(1)
    generator = rasterio.features.shapes(source=array.astype(
        'uint8'), mask=mask.astype('uint8'), transform=dataset.transform)
    features_per_class = {}
    for geom, value in generator:
        geom = shapely.geometry.shape(geom)
        class_ = str(int(value))
        if class_ in features_per_class.keys():
            features_per_class[class_].append(geom)
        else:
            features_per_class[class_] = [geom]
    return features_per_class


def multiPolygon2polygons(geom):
    geoms = [geom]
    if geom.geom_type == "MultiPolygon":
        geoms = list(geom.geoms)
    return geoms


def get_features(features_per_class, area):
    project = partial(
        pyproj.transform,
        pyproj.Proj(fcrs.from_epsg(3857)),
        pyproj.Proj(4326))
    features = []
    for class_ in features_per_class.keys():
        geoms = features_per_class[class_]
        for geom in geoms:
            poly = Polygon(geom.exterior.coords)
            # filter by area
            if poly.area > area:
                # poly = Polygon(geom.exterior.coords)
                geom_reporj = shpTrans(project, geom)
                geom_sorted = shapely.ops.transform(lambda x, y: (y, x), geom_reporj)
                feature = Feature(geometry=geom_sorted, properties={"v": class_})
                features.append(feature)
    return features


def set_classes_values(features, classes):

    for feature in features:
        v = feature["properties"]["v"]
        if v in classes.keys():
            feature["properties"]["class"] = classes[v]

    return features


def simplify_features(features_per_class, buffer, simplify):
    for class_ in features_per_class.keys():
        polys = features_per_class[class_]
        polys_buffer_plus = [p.buffer(buffer, single_sided=True) for p in polys]
        merged_poly = unary_union(polys_buffer_plus)
        polygons_list = multiPolygon2polygons(merged_poly)
        multipolygons_list = [p.buffer(-1 * buffer, single_sided=True) for p in polygons_list]
        polygons_list = list(itertools.chain(
            *[multiPolygon2polygons(p) for p in multipolygons_list]))
        polys_simply = [p.simplify(simplify, preserve_topology=False) for p in polygons_list]

#         ## Smoth
#         polygons_curve = []
#         for poly in polys_simply:
#             multiline = poly.boundary
#             # merged = unary_union(multiline)
#             # print(merged.type)
#             if multiline.type == "LineString":
#                 # l = multiline.parallel_offset(1, quad_segs=20, join_style=1, mitre_limit=20)
#                 l = multiline.parallel_offset(0.00005, 'left', join_style=2)
#                 p = l.convex_hull
#                 polygons_curve.append(p)

        features_per_class[class_] = polys_simply
    return features_per_class
