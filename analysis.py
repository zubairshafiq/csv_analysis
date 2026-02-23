import csv

with open("sales_data.csv", "r", newline="") as file:
    reader = csv.DictReader(file)

    transaction_count = 0
    total_order_quantity = 0
    total_revenue = 0
    total_cost = 0
    total_profit = 0
    total_unit_price = 0

    for row in reader:
        unit_price = int(row["Unit_Price"])
        if unit_price > 100:
            transaction_count += 1
            total_order_quantity += int(row["Order_Quantity"])
            total_revenue += int(row["Revenue"])
            total_cost += int(row["Cost"])
            total_profit += int(row["Profit"])
            total_unit_price += unit_price

    average_unit_price = (
        total_unit_price / transaction_count if transaction_count else 0
    )

    print("Summary for transactions with Unit_Price > 100")
    print(f"Transactions: {transaction_count}")
    print(f"Total Order Quantity: {total_order_quantity}")
    print(f"Total Revenue: {total_revenue}")
    print(f"Total Cost: {total_cost}")
    print(f"Total Profit: {total_profit}")
    print(f"Average Unit Price: {average_unit_price:.2f}")
