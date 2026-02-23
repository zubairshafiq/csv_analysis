# CSV Analysis Plan

1. Import Python's built-in `csv` module.
2. Open `sales_data.csv` in read mode.
3. Create a `csv.reader` object and print only the header row.

```python
import csv

with open("sales_data.csv", "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)
    print(header)
```
