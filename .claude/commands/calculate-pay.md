---
description: Calculate DJ payments for a period
allowed-tools: Read, Write, Glob
argument-hint: [month]
context: fork
model: claude-3-5-haiku-20241022
---

Calculate payments for: $1 (e.g., "2026-03")

## Payment Rates

**DJ Rate:** ~THB 900/hr (net after 5% WHT)
- 3-hour set: Gross THB 2,842.11, WHT THB 142.11, Net THB 2,700
- 2-hour set: Gross THB 1,894.74, WHT THB 94.74, Net THB 1,800

**Charge Rate:** THB 1,030.93/hr (hotel deducts 3% WHT)
- 3-hour day: THB 3,092.78
- 2-hour day: THB 2,061.86

## Instructions

1. Read schedule from `schedules/[month]/`
2. Count shifts per DJ (distinguish 3hr vs 2hr days)
3. Calculate per DJ: total hours, gross, WHT, net
4. Calculate Bright Ears invoice total

## Output

### DJ Payment Summary - [Month]
| DJ | 3hr Sets | 2hr Sets | Total Hours | Gross | WHT | Net |
|---|---|---|---|---|---|---|

### Bright Ears Invoice to ABar
- 3-hour days: X × THB 3,092.78
- 2-hour days: X × THB 2,061.86
- Total: THB X

Save to `payments/[month]-summary.md`
