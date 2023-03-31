import click
from ds-datag.utils import read_geojson, write_geojson


@click.command(short_help="Script to get last updates for adapters")
@click.option(
    "--input_geojson",
    help="Location of input geojson",
    default="points.geojson",
)
@click.option(
    "--output_geojson",
    help="Location of ouput geojson",
    default="output_points.geojson",
)
def main(input_geojson, output_geojson):
    """Start function."""
    new_features = read_geojson(input_geojson)
    write_geojson(output_geojson, new_features)


if __name__ == "__main__":
    main()
