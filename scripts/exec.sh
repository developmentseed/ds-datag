#!/usr/bin/env bash
read_file \
    --input_geojson=https://gist.githubusercontent.com/Rub21/175dde9538c0fb83e584e5f9c098c6ab/raw/5db933c9a0da859ed0c7bc77122afde8881003d9/points.geojson \
    --output_geojson=test.geojson

cat test.geojson
