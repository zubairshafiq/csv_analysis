# csv_analysis

## Overview
`csv_analysis` is a lightweight CSV inspection tool that highlights trends in the provided sales dataset. `analysis.py` scans `sales_data.csv`, filters for transactions whose `Unit_Price` is greater than 100, and emits a human-friendly summary with counts, totals, and averages. The project is intentionally small so it can be used as a learning aid or starting point for more advanced analyses.

## Prerequisites
- Python 3.10 or later (the repo was validated with `Python 3.10.14`).
- No external dependencies beyond the Python standard library.

## Data file
- `sales_data.csv` is a comma-separated export containing columns such as `Date`, `Product`, `Order_Quantity`, `Unit_Cost`, `Unit_Price`, `Profit`, `Cost`, and `Revenue`.
- The CSV carries sales records from 2013 to 2016 across multiple regions, product categories, and customer segments.

## Script details
- `analysis.py` uses `csv.DictReader` so that column values are referenced by name, improving readability and resilience against column order changes.
- The script collects totals only for rows where `Unit_Price > 100`, incrementing counters for transactions, order quantities, revenue, cost, profit, and the unit price sum.
- After processing, it computes the average unit price (with a guard for zero matches) and prints a formatted table with aligned columns and formatted numbers.

## Running the analysis
```bash
python3 analysis.py
```
- The script prints a short header, a metric/value table, and uses commas on the totals for easier reading.
- You can redirect the output if you prefer a file: `python3 analysis.py > unit-price-summary.txt`.

## Output snapshot
```
Summary for transactions with Unit_Price > 100
==============================================
Metric                          Value
-------------------------
Transactions                   27,032
Total Order Quantity           43,620
Total Revenue              62,756,152
Total Cost                 41,701,335
Total Profit               21,054,817
Average Unit Price           1,832.77
```

## Repository layout
- `analysis.py` — analysis script as described above.
- `sales_data.csv` — source dataset used by the script.
- `csv_analysis_plan.md` — notes or future plan (kept for context).

## Next steps
1. Add more filters (by country, product category, etc.) and expose them via CLI arguments.
2. Emit CSV/JSON reports for downstream systems or dashboards.
3. Write tests or sample snapshots to capture changes in the summary logic over time.
