# Advanced Excel Patterns

## Charts

```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

# Bar chart
chart = BarChart()
data = Reference(ws, min_col=2, min_row=1, max_row=10)
categories = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.title = "Sales by Region"
ws.add_chart(chart, "E1")

# Line chart
line = LineChart()
line.add_data(data, titles_from_data=True)
line.set_categories(categories)
ws.add_chart(line, "E15")

# Pie chart
pie = PieChart()
pie.add_data(data, titles_from_data=True)
pie.set_categories(categories)
ws.add_chart(pie, "E30")
```

## Conditional Formatting

```python
from openpyxl.formatting.rule import (
    ColorScaleRule, CellIsRule, FormulaRule
)
from openpyxl.styles import PatternFill

# Color scale (red to green)
rule = ColorScaleRule(
    start_type='min', start_color='FF0000',
    end_type='max', end_color='00FF00'
)
ws.conditional_formatting.add('A1:A10', rule)

# Highlight cells > 100
red_fill = PatternFill(start_color='FF0000', fill_type='solid')
rule = CellIsRule(
    operator='greaterThan', 
    formula=['100'], 
    fill=red_fill
)
ws.conditional_formatting.add('B1:B10', rule)

# Formula-based rule
rule = FormulaRule(
    formula=['$A1>$B1'],
    fill=PatternFill(start_color='FFFF00', fill_type='solid')
)
ws.conditional_formatting.add('A1:B10', rule)
```

## Data Validation

```python
from openpyxl.worksheet.datavalidation import DataValidation

# Dropdown list
dv = DataValidation(
    type="list",
    formula1='"Option1,Option2,Option3"',
    allow_blank=True
)
dv.add('A1:A100')
ws.add_data_validation(dv)

# Number range
dv = DataValidation(
    type="whole",
    operator="between",
    formula1=0,
    formula2=100
)
dv.add('B1:B100')
ws.add_data_validation(dv)
```

## Named Ranges

```python
from openpyxl.workbook.defined_name import DefinedName

# Create named range
ref = "Sheet1!$A$1:$A$10"
defn = DefinedName("SalesData", attr_text=ref)
wb.defined_names.add(defn)

# Use in formula
ws['B1'] = '=SUM(SalesData)'
```

## Freeze Panes

```python
# Freeze top row
ws.freeze_panes = 'A2'

# Freeze first column
ws.freeze_panes = 'B1'

# Freeze top row and first column
ws.freeze_panes = 'B2'
```

## Print Settings

```python
from openpyxl.worksheet.page import PageMargins

# Set print area
ws.print_area = 'A1:G50'

# Repeat rows at top of each page
ws.print_title_rows = '1:1'

# Landscape orientation
ws.page_setup.orientation = 'landscape'

# Fit to one page wide
ws.page_setup.fitToPage = True
ws.page_setup.fitToWidth = 1
ws.page_setup.fitToHeight = 0
```

## Working with Large Files

```python
# Read-only mode for large files
from openpyxl import load_workbook
wb = load_workbook('large.xlsx', read_only=True)

# Write-only mode for generating large files
from openpyxl import Workbook
wb = Workbook(write_only=True)
ws = wb.create_sheet()
for row in data:
    ws.append(row)
wb.save('output.xlsx')
```

## Merged Cells

```python
# Merge
ws.merge_cells('A1:D1')
ws['A1'] = 'Merged Header'

# Unmerge
ws.unmerge_cells('A1:D1')

# Style merged cells (apply to top-left)
ws['A1'].alignment = Alignment(horizontal='center')
```

## Cell Comments

```python
from openpyxl.comments import Comment

comment = Comment('This is a note', 'Author Name')
ws['A1'].comment = comment
```

## Hyperlinks

```python
# External URL
ws['A1'].hyperlink = 'https://example.com'
ws['A1'].value = 'Click here'

# Internal link to another sheet
ws['A2'].hyperlink = '#Sheet2!A1'
ws['A2'].value = 'Go to Sheet2'
```
