---
name: vba-to-python-migration
description: "Migrate VBA macros and Excel workbook logic to Python. Use when asked to convert VBA code to Python, explain legacy VBA macros, modernize Excel-based actuarial workflows, or replace spreadsheet logic with pandas. Trigger phrases: convert VBA, migrate from Excel, VBA to Python, modernize macro, replace spreadsheet, Excel to pandas."
---
# VBA-to-Python Migration Skill

## What This Skill Does
Helps actuarial teams migrate legacy VBA macros and Excel-based workflows to modern Python code while preserving all business logic exactly.

## Workflow

### Step 1: Analyze the VBA Code
- Read and explain the VBA macro in plain language
- Identify the business logic (e.g., rating factors, calculations, lookups)
- Note any Excel-specific operations (cell references, worksheet loops, formatting)

### Step 2: Map VBA Patterns to Python
| VBA Pattern | Python Equivalent |
|-------------|-------------------|
| `Select Case` | Dictionary lookup or `if/elif` chain |
| `For i = 2 To lastRow` | `df.apply()` or vectorized pandas |
| `ws.Cells(i, j).Value` | `df.iloc[i, j]` or `df["column"]` |
| `Round(x, 2)` | `round(x, 2)` |
| `UCase(str)` | `str.upper()` |
| `MsgBox` | `print()` |
| `Dim x As Double` | Type hint `x: float` |

### Step 3: Write the Python Version
- Use pandas DataFrames instead of worksheet loops
- Convert lookup functions to use dictionaries for clarity
- Add type hints to function signatures
- Preserve the exact same calculation logic — do NOT optimize during migration

### Step 4: Add Unit Tests
- Write tests that verify the Python output matches the VBA output for known inputs
- Test boundary conditions (edge of Select Case ranges)
- Test unknown/default values

### Step 5: Document the Migration
- Note any behavioral differences (e.g., rounding, null handling)
- Show before/after comparison for key functions

## Constraints
- **Never change the business logic** — the migration must be exact
- Round to the same precision as the VBA original
- Handle the same edge cases (minimum premium, unknown state defaults, etc.)
