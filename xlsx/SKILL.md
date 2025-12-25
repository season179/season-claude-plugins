---
name: xlsx
description: "Reads, creates, edits, and analyzes Excel spreadsheets with full formula support, formatting, charts, and data validation. Triggers when working with .xlsx, .xlsm, .xls, .csv, or .tsv files for data analysis, spreadsheet creation, formula-based models, or modifying existing workbooks."
---

# Excel File Operations

## Dependencies

```bash
pip install openpyxl pandas
```

Formula recalculation requires LibreOffice:
- macOS: `brew install --cask libreoffice`
- Linux: `sudo apt install libreoffice xvfb`

## Core Rule: Excel Formulas Over Python Calculations

```python
# ❌ Wrong
total = df['Sales'].sum()
ws['B10'] = total

# ✅ Correct
ws['B10'] = '=SUM(B2:B9)'
```

## Library Selection

| Use Case | Library |
|----------|---------|
| Data analysis, bulk operations | pandas |
| Formulas, formatting, Excel features | openpyxl |

## Reading

```python
import pandas as pd
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)
```

```python
from openpyxl import load_workbook
wb = load_workbook('file.xlsx')  # Preserves formulas
wb = load_workbook('file.xlsx', data_only=True)  # Values only
# WARNING: Saving after data_only=True loses all formulas permanently
```

## Creating

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws.title = "Data"

ws['A1'] = 'Revenue'
ws['B1'] = 100000
ws['B2'] = '=B1*1.1'

ws['A1'].font = Font(bold=True)
ws.column_dimensions['A'].width = 15

wb.save('output.xlsx')
```

## Editing

```python
from openpyxl import load_workbook

wb = load_workbook('existing.xlsx')
ws = wb.active

ws['A1'] = 'Updated'
ws.insert_rows(2)
ws.delete_cols(3)

new_ws = wb.create_sheet('NewSheet')
wb.save('modified.xlsx')
```

## Formula Workflow (with validation)

Copy this checklist for formula-based files:

```
Excel Formula Task:
- [ ] Step 1: Create/load workbook
- [ ] Step 2: Add data and formulas
- [ ] Step 3: Save file
- [ ] Step 4: Run recalc.py
- [ ] Step 5: Check for errors, fix if needed
- [ ] Step 6: Repeat steps 4-5 until status=success
```

**Step 4: Recalculate formulas**

```bash
python scripts/recalc.py output.xlsx
```

**Step 5: Check output**

Success:
```json
{"status": "success", "total_errors": 0, "total_formulas": 42}
```

Errors found:
```json
{
  "status": "errors_found",
  "total_errors": 2,
  "error_summary": {
    "#REF!": {"count": 2, "locations": ["Sheet1!B5", "Sheet1!C10"]}
  }
}
```

If errors found, fix the formula issues and run recalc.py again.

## Common Operations

### Iterate cells
```python
for row in ws.iter_rows(min_row=1, max_row=10):
    for cell in row:
        print(cell.value)
```

### Merge cells
```python
ws.merge_cells('A1:D1')
```

### Cell formatting
```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

ws['A1'].font = Font(bold=True, color='FF0000', size=14)
ws['A1'].fill = PatternFill('solid', fgColor='FFFF00')
ws['A1'].alignment = Alignment(horizontal='center', vertical='center')
ws['A1'].border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
```

### Number formats
```python
ws['A1'].number_format = '$#,##0.00'      # Currency
ws['B1'].number_format = '0.0%'           # Percentage
ws['C1'].number_format = '#,##0;(#,##0)'  # Negative in parens
```

## Error Prevention

- Cell indices are 1-based (A1 = row 1, column 1)
- Cross-sheet references: `Sheet1!A1`
- Always run recalc.py before delivering formula-based files
- Test formulas on 2-3 cells before applying broadly

## Advanced Topics

- **Charts, conditional formatting, data validation**: See [references/advanced-patterns.md](references/advanced-patterns.md)
- **Financial modeling conventions**: See [references/financial-models.md](references/financial-models.md)
