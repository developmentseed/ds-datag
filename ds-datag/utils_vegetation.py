def get_ndvi(dataArray):
    red = dataArray[0]
    nir = dataArray[1]
    ndvi = (nir.astype(float) - red.astype(float)) / (nir + red)
    return ndvi


def filter_grassland_shrup(dataArray):
    d = dataArray.where(dataArray > 0.18 , 0)
    d = d.where(d < 0.27 , 0)
    # print(d.max())
    # print(d.min())
    return d


def filter_dense_vegetation(dataArray):
    d = dataArray.where(dataArray > 0.50 , 0)
    d = d.where(d < 1 , 0)
    return d
