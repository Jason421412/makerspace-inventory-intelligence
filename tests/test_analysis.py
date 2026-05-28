import unittest

from makerspace_inventory.analysis import infer_category, rank_followups, summarize
from makerspace_inventory.models import InventoryItem


class AnalysisTests(unittest.TestCase):
    def test_infers_domain_categories(self):
        self.assertEqual(infer_category("Arduino Uno"), "microcontroller")
        self.assertEqual(infer_category("Soil moisture sensor"), "sensor")
        self.assertEqual(infer_category("CO2 Laser Cutter"), "fabrication")

    def test_summary_counts_statuses_and_followups(self):
        items = [
            InventoryItem(asset_id="A1", name="Arduino Uno", status="Complete"),
            InventoryItem(asset_id="A2", name="Missing motor", status="Missing", notes="1 missing"),
            InventoryItem(asset_id="A3", name="Unknown sensor", status="Unknown"),
        ]
        result = summarize(items)
        self.assertEqual(result["total_assets"], 3)
        self.assertEqual(result["status_counts"]["complete"], 1)
        self.assertEqual(result["follow_up_count"], 2)

    def test_ranks_missing_items_first(self):
        items = [
            InventoryItem(asset_id="A1", name="Recorded item", status="recorded", location="Shelf"),
            InventoryItem(asset_id="A2", name="Missing motor", status="Missing", notes="1 missing"),
        ]
        ranked = rank_followups(items)
        self.assertEqual(ranked[0][1].asset_id, "A2")


if __name__ == "__main__":
    unittest.main()
