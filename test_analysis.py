import csv
import tempfile
import unittest
from pathlib import Path

import analysis


class AnalysisTests(unittest.TestCase):
    def _write_csv(self, rows):
        headers = [
            "Unit_Price",
            "Order_Quantity",
            "Revenue",
            "Cost",
            "Profit",
        ]
        tmp = tempfile.NamedTemporaryFile(mode="w", newline="", suffix=".csv", delete=False)
        with tmp:
            writer = csv.DictWriter(tmp, fieldnames=headers)
            writer.writeheader()
            writer.writerows(rows)
        self.addCleanup(lambda: Path(tmp.name).unlink(missing_ok=True))
        return tmp.name

    def test_summarize_transactions_filters_and_aggregates(self):
        csv_path = self._write_csv(
            [
                {
                    "Unit_Price": 150,
                    "Order_Quantity": 2,
                    "Revenue": 300,
                    "Cost": 200,
                    "Profit": 100,
                },
                {
                    "Unit_Price": 90,
                    "Order_Quantity": 5,
                    "Revenue": 450,
                    "Cost": 350,
                    "Profit": 100,
                },
                {
                    "Unit_Price": 120,
                    "Order_Quantity": 1,
                    "Revenue": 120,
                    "Cost": 60,
                    "Profit": 60,
                },
            ]
        )

        summary = analysis.summarize_transactions(csv_path, min_unit_price=100)

        self.assertEqual(summary["transactions"], 2)
        self.assertEqual(summary["total_order_quantity"], 3)
        self.assertEqual(summary["total_revenue"], 420)
        self.assertEqual(summary["total_cost"], 260)
        self.assertEqual(summary["total_profit"], 160)
        self.assertAlmostEqual(summary["average_unit_price"], 135.0)

    def test_summarize_transactions_returns_zero_average_when_no_match(self):
        csv_path = self._write_csv(
            [
                {
                    "Unit_Price": 10,
                    "Order_Quantity": 3,
                    "Revenue": 30,
                    "Cost": 20,
                    "Profit": 10,
                }
            ]
        )

        summary = analysis.summarize_transactions(csv_path, min_unit_price=100)

        self.assertEqual(summary["transactions"], 0)
        self.assertEqual(summary["total_order_quantity"], 0)
        self.assertEqual(summary["total_revenue"], 0)
        self.assertEqual(summary["total_cost"], 0)
        self.assertEqual(summary["total_profit"], 0)
        self.assertEqual(summary["average_unit_price"], 0)

    def test_load_unit_prices_reads_all_rows(self):
        csv_path = self._write_csv(
            [
                {
                    "Unit_Price": 11,
                    "Order_Quantity": 1,
                    "Revenue": 11,
                    "Cost": 8,
                    "Profit": 3,
                },
                {
                    "Unit_Price": 22,
                    "Order_Quantity": 2,
                    "Revenue": 44,
                    "Cost": 30,
                    "Profit": 14,
                },
            ]
        )

        self.assertEqual(analysis.load_unit_prices(csv_path), [11, 22])

    def test_write_histogram_svg_writes_file_with_expected_bars(self):
        unit_prices = [10, 20, 20, 30]
        tmp_svg = tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False)
        tmp_svg.close()
        self.addCleanup(lambda: Path(tmp_svg.name).unlink(missing_ok=True))

        analysis.write_unit_price_histogram_svg(unit_prices, tmp_svg.name, bins=4)

        svg = Path(tmp_svg.name).read_text(encoding="utf-8")
        self.assertIn("<svg", svg)
        self.assertIn("Distribution of Unit_Price", svg)
        self.assertEqual(svg.count("fill='#2563eb'"), 4)

    def test_write_histogram_svg_raises_for_empty_input(self):
        tmp_svg = tempfile.NamedTemporaryFile(mode="w", suffix=".svg", delete=False)
        tmp_svg.close()
        self.addCleanup(lambda: Path(tmp_svg.name).unlink(missing_ok=True))

        with self.assertRaises(ValueError):
            analysis.write_unit_price_histogram_svg([], tmp_svg.name)


if __name__ == "__main__":
    unittest.main()
