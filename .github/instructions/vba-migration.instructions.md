---
applyTo: "**/*.vba"
description: "Use when working with VBA files: migration to Python, explaining legacy macros, Excel automation code, rating workbooks"
---
# VBA Migration Guidelines

When working with VBA files in this actuarial project:

## Understanding Legacy VBA
- VBA macros in actuarial workbooks typically perform: premium rating, triangle manipulation, data aggregation, report generation
-  statements = Python  chains or dictionary lookups
-  loops over worksheet rows = pandas DataFrame operations
- Cell references like  = column-based DataFrame access
-  = Python type hints (encouraged but not enforced)

## Migration Patterns
- Replace row-by-row worksheet loops with vectorized pandas operations
- Convert  lookups to Python dictionaries for cleaner code
- Replace VBA  with Python  -- note banker's rounding difference
- Preserve all business logic exactly -- do not "optimize" the rating algorithm during migration
- Add unit tests for every migrated function to verify equivalence

## Common VBA-to-Python Mappings
| VBA | Python |
|-----|--------|
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
|  |  |
