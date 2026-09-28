# Intern ID - 9018
# Inventory Stock Level Audit

## Objective
Audit stock levels and identify products that may need replenishment or may be overstocked.

## Methodology
1. Calculate inventory value.
2. Estimate days of stock.
3. Compare current stock with reorder and maximum-stock thresholds.
4. Classify SKUs as REORDER, NORMAL or OVERSTOCK.
5. Summarize inventory by category.
6. Visualize inventory value and status.

## Technology
Python, Pandas, Matplotlib.

## Run
```bash
pip install -r requirements.txt
python src/analysis.py
```

Generated files appear in `outputs/`.
