# Financial Model Standards

## Color Coding (Industry Standard)

| Color | RGB | Meaning |
|-------|-----|---------|
| Blue text | (0,0,255) | Hardcoded inputs |
| Black text | (0,0,0) | Formulas/calculations |
| Green text | (0,128,0) | Links to other sheets |
| Red text | (255,0,0) | External file links |
| Yellow background | (255,255,0) | Key assumptions |

```python
from openpyxl.styles import Font, PatternFill

# Input cells (blue)
cell.font = Font(color='0000FF')

# Formula cells (black)  
cell.font = Font(color='000000')

# Cross-sheet links (green)
cell.font = Font(color='008000')

# External links (red)
cell.font = Font(color='FF0000')

# Key assumptions (yellow background)
cell.fill = PatternFill('solid', fgColor='FFFF00')
```

## Number Formatting

| Type | Format | Example |
|------|--------|---------|
| Currency | `$#,##0` | $1,234 |
| Percentages | `0.0%` | 12.5% |
| Multiples | `0.0x` | 3.2x |
| Negatives | `(#,##0)` | (500) |
| Zeros | `-` via format | - |
| Years | Text | "2024" |

```python
# Currency with units in header
ws['A1'] = 'Revenue ($mm)'
ws['A1'].number_format = '$#,##0'

# Percentage
ws['B1'].number_format = '0.0%'

# Negative in parentheses, zero as dash
ws['C1'].number_format = '$#,##0;($#,##0);"-"'

# Year as text (prevents "2,024")
ws['D1'] = '2024'
ws['D1'].number_format = '@'
```

## Formula Best Practices

### Use Cell References for Assumptions

```python
# ❌ Wrong: hardcoded growth rate
ws['B3'] = '=B2*1.05'

# ✅ Correct: reference assumption cell
ws['A1'] = 'Growth Rate'
ws['B1'] = 0.05  # Blue text - input
ws['B3'] = '=B2*(1+$B$1)'  # Black text - formula
```

### Document Hardcoded Sources

Add comments or adjacent cells with sources:

```
Source: Company 10-K, FY2024, Page 45
Source: Bloomberg Terminal, 2025-08-15, AAPL US Equity
Source: FactSet Consensus Estimates, 2025-08-20
```

## Model Structure Template

```
Sheet 1: Assumptions
- All inputs in one place
- Blue text for all hardcodes
- Yellow highlight for key drivers

Sheet 2: Historical Data
- Source data with documentation
- No formulas except data validation

Sheet 3: Projections
- All cells are formulas (black text)
- Reference assumptions sheet
- Green text for cross-sheet links

Sheet 4: Outputs/Summary
- Key metrics and ratios
- Charts and visualizations
```
