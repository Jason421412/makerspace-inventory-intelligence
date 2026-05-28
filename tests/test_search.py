import unittest

from makerspace_inventory.search import search_items
from makerspace_inventory.models import InventoryItem


class SearchTests(unittest.TestCase):
    def test_search_prioritizes_exact_name_terms(self):
        items = [
            InventoryItem(asset_id="5.0.1", name="ARDUINO UNO", location="Shelf 3"),
            InventoryItem(asset_id="13.1.1", name="3D PRINTER FILAMENT", location="Shelf 2"),
        ]
        results = search_items(items, "arduino", limit=1)
        self.assertEqual(results[0][1].asset_id, "5.0.1")

    def test_search_can_match_location(self):
        items = [
            InventoryItem(asset_id="A", name="Battery", location="Shelf Lvl 4"),
            InventoryItem(asset_id="B", name="Battery", location="Cupboard 2"),
        ]
        results = search_items(items, "cupboard", limit=1)
        self.assertEqual(results[0][1].asset_id, "B")


if __name__ == "__main__":
    unittest.main()
