import csv

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
