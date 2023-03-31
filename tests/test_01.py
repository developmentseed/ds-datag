import sys
import unittest
from ds-datag.utils import read_geojson

sys.path.append("..")


class Test_geojson(unittest.TestCase):
    """Testing reading geojson."""

    def test_geojson(self):
        """Test geojson reading and writing."""
        features = read_geojson("tests/fixtures/points.geojson")
        self.assertEqual(len(features), 2)
