import csv
from math import ceil

# Open the CSV data file and parse rows as dictionaries keyed by column names.
with open("sales_data.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    # Initialize summary counters for transactions with Unit_Price > 100.
    transaction_count = 0
    total_order_quantity = 0
    total_revenue = 0
    total_cost = 0
    total_profit = 0
    total_unit_price = 0

    # Scan each transaction and include it in totals only if Unit_Price is above 100.
    for row in reader:
        unit_price = int(row["Unit_Price"])
        if unit_price > 100:
            transaction_count += 1
            total_order_quantity += int(row["Order_Quantity"])
            total_revenue += int(row["Revenue"])
            total_cost += int(row["Cost"])
            total_profit += int(row["Profit"])
            total_unit_price += unit_price

    # Avoid division by zero if no rows match the filter.
    average_unit_price = (
        total_unit_price / transaction_count if transaction_count else 0
    )

    # Print the final summary for matching transactions.
    title = "Summary for transactions with Unit_Price > 100"
    print(title)
    print("=" * len(title))
    print(f"{'Metric':<25}{'Value':>12}")
    print("-------------------------" + " " * 12)
    print(f"{'Transactions':<25}{transaction_count:>12,}")
    print(f"{'Total Order Quantity':<25}{total_order_quantity:>12,}")
    print(f"{'Total Revenue':<25}{total_revenue:>12,}")
    print(f"{'Total Cost':<25}{total_cost:>12,}")
    print(f"{'Total Profit':<25}{total_profit:>12,}")
    print(f"{'Average Unit Price':<25}{average_unit_price:>12,.2f}")


def write_unit_price_histogram_svg(unit_prices, output_path, bins=24):
    if not unit_prices:
        raise ValueError("No Unit_Price values found in sales_data.csv")

    width = 980
    height = 560
    margin_left = 70
    margin_right = 30
    margin_top = 50
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    min_price = min(unit_prices)
    max_price = max(unit_prices)
    span = max(max_price - min_price, 1)
    bin_width = span / bins

    counts = [0] * bins
    for price in unit_prices:
        index = int((price - min_price) / bin_width)
        if index >= bins:
            index = bins - 1
        counts[index] += 1

    max_count = max(counts)
    bar_width = plot_width / bins

    lines = []
    lines.append(
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>"
    )
    lines.append(
        "<rect x='0' y='0' width='100%' height='100%' fill='#fcfcfd' />"
    )
    lines.append(
        "<text x='490' y='28' text-anchor='middle' font-family='Arial' font-size='20' "
        "font-weight='bold' fill='#1f2937'>Distribution of Unit_Price</text>"
    )

    # Axes
    x0 = margin_left
    y0 = height - margin_bottom
    x1 = width - margin_right
    y1 = margin_top
    lines.append(
        f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#374151' stroke-width='1.5' />"
    )
    lines.append(
        f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#374151' stroke-width='1.5' />"
    )

    # Y ticks
    y_ticks = 5
    for i in range(y_ticks + 1):
        value = int(round(max_count * i / y_ticks))
        y = y0 - (plot_height * i / y_ticks)
        lines.append(
            f"<line x1='{x0 - 6}' y1='{y:.2f}' x2='{x0}' y2='{y:.2f}' stroke='#4b5563' stroke-width='1' />"
        )
        lines.append(
            f"<text x='{x0 - 10}' y='{y + 4:.2f}' text-anchor='end' font-family='Arial' "
            f"font-size='12' fill='#4b5563'>{value}</text>"
        )
        lines.append(
            f"<line x1='{x0}' y1='{y:.2f}' x2='{x1}' y2='{y:.2f}' stroke='#e5e7eb' stroke-width='1' />"
        )

    # X ticks
    x_ticks = 6
    for i in range(x_ticks + 1):
        value = int(round(min_price + (span * i / x_ticks)))
        x = x0 + (plot_width * i / x_ticks)
        lines.append(
            f"<line x1='{x:.2f}' y1='{y0}' x2='{x:.2f}' y2='{y0 + 6}' stroke='#4b5563' stroke-width='1' />"
        )
        lines.append(
            f"<text x='{x:.2f}' y='{y0 + 24}' text-anchor='middle' font-family='Arial' "
            f"font-size='12' fill='#4b5563'>{value}</text>"
        )

    # Bars
    for i, count in enumerate(counts):
        bar_height = 0 if max_count == 0 else (count / max_count) * plot_height
        x = x0 + i * bar_width + 1
        y = y0 - bar_height
        w = max(bar_width - 2, 1)
        lines.append(
            f"<rect x='{x:.2f}' y='{y:.2f}' width='{w:.2f}' height='{bar_height:.2f}' "
            "fill='#2563eb' opacity='0.85' />"
        )

    lines.append(
        "<text x='490' y='545' text-anchor='middle' font-family='Arial' font-size='13' "
        "fill='#374151'>Unit_Price</text>"
    )
    lines.append(
        f"<text x='22' y='{margin_top + plot_height / 2:.2f}' text-anchor='middle' "
        "font-family='Arial' font-size='13' fill='#374151' transform='rotate(-90 22 "
        f"{margin_top + plot_height / 2:.2f})'>Frequency</text>"
    )
    lines.append("</svg>")

    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.write("\n".join(lines))


with open("sales_data.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    unit_prices = [int(row["Unit_Price"]) for row in reader]

write_unit_price_histogram_svg(unit_prices, "unit_price_distribution.svg")
print("Saved histogram to unit_price_distribution.svg")
