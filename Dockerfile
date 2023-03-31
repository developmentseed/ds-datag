FROM continuumio/miniconda3:4.10.3p1

RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

RUN conda install -c conda-forge \
    requests \
    joblib \
    tqdm \
    click \
    smart-open \
    geojson \
    gdal \
    shapely \
    pre-commit \
    geopandas \
    rioxarray \
    rasterio \
    scikit-learn \
    jupyterlab_widgets  \
    jupyterlab \
    pystac-client \
    # planetary_computer \
    geopandas \
    contextily \
    earthpy \
    geojson \
    supermercado

CMD ["/bin/bash", "-c", "jupyter lab --allow-root --no-browser --ip 0.0.0.0 --port 8888 --notebook-dir=/mnt"]
