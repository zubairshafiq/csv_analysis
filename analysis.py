import csv


def summarize_transactions(csv_path, min_unit_price=100):
    """Compute summary metrics for rows where Unit_Price is above min_unit_price."""
    transaction_count = 0
    total_order_quantity = 0
    total_revenue = 0
    total_cost = 0
    total_profit = 0
    total_unit_price = 0

    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            unit_price = int(row["Unit_Price"])
            if unit_price > min_unit_price:
                transaction_count += 1
                total_order_quantity += int(row["Order_Quantity"])
                total_revenue += int(row["Revenue"])
                total_cost += int(row["Cost"])
                total_profit += int(row["Profit"])
                total_unit_price += unit_price

    average_unit_price = (
        total_unit_price / transaction_count if transaction_count else 0
    )
    return {
        "transactions": transaction_count,
        "total_order_quantity": total_order_quantity,
        "total_revenue": total_revenue,
        "total_cost": total_cost,
        "total_profit": total_profit,
        "average_unit_price": average_unit_price,
    }


def print_summary(summary, min_unit_price=100):
    """Print a formatted summary table for aggregate metrics."""
    title = f"Summary for transactions with Unit_Price > {min_unit_price}"
    print(title)
    print("=" * len(title))
    print(f"{'Metric':<25}{'Value':>12}")
    print("-------------------------" + " " * 12)
    print(f"{'Transactions':<25}{summary['transactions']:>12,}")
    print(f"{'Total Order Quantity':<25}{summary['total_order_quantity']:>12,}")
    print(f"{'Total Revenue':<25}{summary['total_revenue']:>12,}")
    print(f"{'Total Cost':<25}{summary['total_cost']:>12,}")
    print(f"{'Total Profit':<25}{summary['total_profit']:>12,}")
    print(f"{'Average Unit Price':<25}{summary['average_unit_price']:>12,.2f}")


def load_unit_prices(csv_path):
    """Load all Unit_Price values from the CSV as integers."""
    with open(csv_path, "r", newline="") as file:
        reader = csv.DictReader(file)
        return [int(row["Unit_Price"]) for row in reader]


def write_unit_price_histogram_svg(unit_prices, output_path, bins=24):
    # The histogram needs at least one value; fail fast with a clear message.
    if not unit_prices:
        raise ValueError("No Unit_Price values found in sales_data.csv")

    # Overall SVG canvas and chart margins.
    # The plot area is the inner rectangle where axes, ticks, and bars are drawn.
    width = 980
    height = 560
    margin_left = 70
    margin_right = 30
    margin_top = 50
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    # Determine data range and split it into equally sized bins.
    # span is forced to at least 1 so bin_width never becomes zero.
    min_price = min(unit_prices)
    max_price = max(unit_prices)
    span = max(max_price - min_price, 1)
    bin_width = span / bins

    # Count how many values fall into each bin.
    # A max value can land exactly on the upper boundary due to floating-point math,
    # so we clamp it to the final bin index.
    counts = [0] * bins
    for price in unit_prices:
        index = int((price - min_price) / bin_width)
        if index >= bins:
            index = bins - 1
        counts[index] += 1

    # Scaling factors for vertical bar heights and horizontal bar width.
    max_count = max(counts)
    bar_width = plot_width / bins

    # Build SVG markup as a list of lines, then join once at the end.
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

    # Axis endpoints:
    # (x0, y0) is the bottom-left of the plot area.
    # (x1, y1) are right and top boundaries used for drawing axes/gridlines.
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

    # Y-axis ticks and horizontal grid lines.
    # The labels are frequencies (counts), from 0 up to max_count.
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

    # X-axis ticks spread evenly across the Unit_Price range.
    # Labels are representative values across the min-to-max span.
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

    # Draw each bar using bin counts.
    # Height is normalized by max_count so the tallest bar fills plot_height.
    # A 1px inset keeps neighboring bars visually separated.
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

    # Write the final SVG document to disk.
    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.write("\n".join(lines))


def main():
    csv_path = "sales_data.csv"
    output_svg_path = "unit_price_distribution.svg"

    summary = summarize_transactions(csv_path, min_unit_price=100)
    print_summary(summary, min_unit_price=100)

    unit_prices = load_unit_prices(csv_path)
    write_unit_price_histogram_svg(unit_prices, output_svg_path)
    print(f"Saved histogram to {output_svg_path}")


if __name__ == "__main__":
    main()
