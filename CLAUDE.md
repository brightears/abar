# Bright Ears DJ Management - ABar

## Project Overview

Bright Ears Co., Ltd. manages DJ entertainment at ABar, a high-end Bangkok bar venue.

**Customer:** TCC Hotel Asset Management Co., Ltd.

---

## Venue & Schedule

| Venue | Hours | DJs per Night | Total Hours |
|-------|-------|---------------|-------------|
| ABar | 21:00-24:00 | 1 | 3 hours |

**Default performance:** 3 hours/night, 7 nights/week

### Variable Hours (by month)

**March 2026:**
- **Sun-Wed:** 3 hours (21:00-24:00)
- **Thu-Sat:** 2 hours (22:00-24:00)

*Hours may revert to 3 hours every day from April onwards.*

---

## Music Guidelines

### ABar (Manager: Khun Au)
- **Style:** Open format leaning electronic
- **Core Genres:** Organic House, Afro House, Soulful House, Indie Dance
- **Approach:** Flexible — adjusted in line with guest profiles
- **Vibe:** Sophisticated bar atmosphere

---

## Key Contacts

| Name | Role |
|------|------|
| **Khun Au** | ABar Manager |
| **Khun Tk** | Assistant Bar Manager |

---

## Payment Structure

### Bright Ears Invoices to TCC Hotel Asset Management

**Hourly charge rate:** THB 1,030.93/hr (incorporates 3% WHT deduction by hotel)

| Hours | Charge Amount | How Calculated |
|-------|--------------|----------------|
| 3 hours | THB 3,092.78 | 3 × THB 1,030.93 |
| 2 hours | THB 2,061.86 | 2 × THB 1,030.93 |

*The charge is designed so that after the hotel deducts 3% WHT, Bright Ears receives THB 1,000/hr net.*

**Tax handling:**
- Invoice amount: As above (no separate VAT line)
- Hotel deducts: 3% WHT

### Bright Ears Pays DJs
- **Rate:** THB 900/hr (net after WHT)
- **Deduction:** 5% withholding tax

### DJ Earnings per Set
| Set Length | Gross | WHT 5% | Net |
|------------|-------|--------|-----|
| 3 hours | 2,842.11 | 142.11 | 2,700 |
| 2 hours | 1,894.74 | 94.74 | 1,800 |

### Monthly Invoice Timeline
- **Submit invoice:** By 30th of each month
- **Payment received:** By 25th of following month

---

## Operational Rules

- **Schedule changes:** 48 hours advance notice required
- **Weather cancellation:** 3 hours notice, no charge
- **Equipment:** Provided by venue
- **Dress code:** Private attire matching venue concept

---

## File Organization

```
ABar/
├── CLAUDE.md                # This file - project knowledge
├── contracts/               # Signed agreements
├── djs/
│   ├── profiles/           # Individual DJ profile docs (markdown)
│   └── images/             # DJ photos (promotional use)
├── schedules/
│   └── 2026-03/            # Monthly schedule folders
├── presentations/           # Venue presentations (HTML → PDF)
│   ├── dj-roster-presentation.html/pdf
│   └── march-2026-schedule.html/pdf
├── payments/
│   ├── scripts/
│   │   ├── generate_invoice.py   # Invoice generator
│   │   └── fill_wht_form.py      # WHT form filler (pypdf)
│   ├── templates/
│   │   ├── invoice-template.html # Invoice HTML/CSS template
│   │   └── wht-{dj}.pdf         # DJ WHT templates
│   ├── invoice_config.json       # Tracks invoice numbers (starts #3026)
│   └── {YYYY-MM}/               # Monthly output folders
├── branding/                # Bright Ears logo & brand guide
└── .claude/
    ├── commands/            # Slash commands (user-invoked)
    └── agents/              # Subagents (auto-delegated)
```

---

## Available Subagents

Claude will automatically delegate to these based on task context:

| Subagent | Model | Triggers On |
|----------|-------|-------------|
| `dj-profiler` | Sonnet | Processing DJ info, creating profiles |
| `schedule-builder` | Opus | Creating/managing monthly schedules |
| `presentation-builder` | Opus | Building DJ presentations for venues |
| `payment-calculator` | Sonnet | Calculating payments, generating summaries |

---

## Available Slash Commands

| Command | Purpose |
|---------|---------|
| `/add-dj [name]` | Quick DJ profile creation |
| `/list-djs` | Show roster |
| `/build-presentation` | Generate DJ presentation |
| `/schedule [month]` | View/create schedules |
| `/calculate-pay [month]` | Calculate DJ payments |
| `/project-status` | Quick status overview |

---

## DJ Profile Template

When adding a new DJ, create a markdown file in `djs/profiles/` with:
- Stage name / Real name
- Photo filename (stored in `djs/images/`)
- Music genres/specialties
- Brief bio
- Contact info
- Availability notes

---

## Bright Ears Branding

**Website:** https://brightears.io

### Logo
- **Primary:** `branding/BE_Logo_Transparent.png` - High-res with "BRIGHTEARS" text, transparent background
- **Icon only:** `branding/BE_Logo_White.jpg` - Circle mark only, for small uses
- **Style:** Circular "BE" monogram with cyan ring, white text on transparent/dark

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Brand Cyan | `#00bbe4` | Primary accent, highlights |
| Deep Teal | `#2f6364` | Secondary accent, headers |
| Soft Lavender | `#d59ec9` | Tertiary (use sparingly) |
| Earthy Brown | `#a47764` | Warm accent |
| Luxury Black | `#0a0a0a` | Dark backgrounds |
| Off-White | `#f7f7f7` | Light backgrounds |
| Dark Gray | `#333333` | Body text |

### Typography
- **Headlines:** Playfair (elegant serif)
- **Body:** Inter (modern sans-serif)

### Visual Style
- Modern luxury aesthetic
- Glassmorphism (backdrop blur, translucent cards)
- Gradient overlays (cyan → teal → lavender)
- Soft shadows, rounded corners
- High contrast light/dark sections

---

## Common Mistakes to Avoid

- Do NOT schedule changes without 48 hours notice
- Do NOT miss invoice deadline (30th of month)
- Do NOT forget to match DJ aesthetic to venue
- Do NOT confuse 2-hour vs 3-hour days when calculating charges

---

## Current Status

- **Start date:** TBD (existing customer — venue already active)
- **Today:** March 3, 2026

### Current DJ Roster (5 DJs)

| DJ | Style | Notes |
|---|---|---|
| Benji | Afro/Organic House | Also plays NOBU + LDK |
| UFO | Afro/Organic/Soulful House | Also plays NOBU |
| Linze | International Pop/Open Format/Dance | Also plays NOBU + LDK |
| Scotty B | Open Format/Nu Disco (30+ yrs) | Also plays LDK |
| DJ Pound | Open Format/Pop Charts/R&B/Hip Hop (20 yrs) | Also plays LDK |

---

## DJ Availability Summary

| DJ | Assigned Days | Set Length |
|----|--------------|------------|
| Benji | Thu, Sat | 2 hrs |
| UFO | Tue | 3 hrs |
| Linze | Mon | 3 hrs |
| Scotty B | Wed | 3 hrs |
| DJ Pound | Sun, Fri | 3 hrs / 2 hrs |

---

## March 2026 Schedule (CONFIRMED)

### Weekly Assignments

| Day | DJ | Hours | Duration |
|-----|-----|-------|----------|
| **Monday** | Linze | 21:00-24:00 | 3 hrs |
| **Tuesday** | UFO | 21:00-24:00 | 3 hrs |
| **Wednesday** | Scotty B | 21:00-24:00 | 3 hrs |
| **Thursday** | Benji | 22:00-24:00 | 2 hrs |
| **Friday** | Pound | 22:00-24:00 | 2 hrs |
| **Saturday** | Benji | 22:00-24:00 | 2 hrs |
| **Sunday** | Pound | 21:00-24:00 | 3 hrs |

**All slots filled.** Pound covers both Sundays and Fridays.

### Shift Counts (March)

| DJ | Shifts | Hours |
|----|--------|-------|
| Benji | 8 (4 Thu + 4 Sat) | 16 hrs (all 2-hr sets) |
| UFO | 5 (5 Tue) | 15 hrs (all 3-hr sets) |
| Linze | 5 (5 Mon) | 15 hrs (all 3-hr sets) |
| Scotty B | 4 (4 Wed) | 12 hrs (all 3-hr sets) |
| Pound | 9 (5 Sun + 4 Fri) | 23 hrs (15 × 3-hr + 8 × 2-hr) |
| **Total** | **31** | **81 hrs** |

### Hours Pattern (March)
- **Sun-Wed:** 3 hours (21:00-24:00) — THB 3,092.78
- **Thu-Sat:** 2 hours (22:00-24:00) — THB 2,061.86

### Schedule & Presentation Files
- `schedules/2026-03/march-schedule.md` - Full calendar details with shift counts
- `presentations/march-2026-schedule.html` / `.pdf` - 3-page visual schedule (cover + calendar + lineup)
- `presentations/dj-roster-presentation.html` / `.pdf` - 10-slide DJ introduction deck

---

### Pending Items
- [x] Confirm Friday DJ assignment for March — **DJ Pound assigned**
- [ ] Generate first invoice (#3026)
- [ ] Add any additional DJs to roster

### Completed
- [x] Project folder structure created (Mar 3, 2026)
- [x] CLAUDE.md created with project knowledge
- [x] 5 DJ profiles copied from NOBU project (Benji, UFO, Linze, Scotty B, DJ Pound)
- [x] Branding assets copied
- [x] Payment infrastructure set up (invoice script, WHT templates)
- [x] Subagents configured (4)
- [x] Slash commands created (6)
- [x] **March 2026 schedule created** (Mar 3, 2026) - 31/31 slots filled. Pound 9 (Sun+Fri), Benji 8 (Thu+Sat), UFO 5, Linze 5, Scotty B 4.
- [x] **Presentations created** (Mar 3, 2026) - DJ roster (10 slides) + March schedule (3 pages). HTML + PDF.
- [x] **Calendar dates corrected** (Mar 3, 2026) - Mar 1 = Sunday (was incorrectly Saturday). Shift counts updated.

---

### Technical Notes
- Presentations generated via HTML → Chrome headless → PDF
- Command: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --print-to-pdf="<output>.pdf" --no-margins --print-to-pdf-no-header "file://<input>.html"`

### Invoice Auto-Generation

**Usage:**
```bash
cd payments && source ../.venv/bin/activate

python3 scripts/generate_invoice.py 2026-03                    # March invoice
python3 scripts/generate_invoice.py 2026-03 --dry-run          # preview only

# Adjustment flags:
#   --no-day 15              full day cancellation (no charge)
#   --credit "18:1:Reason"   partial hour deduction
#   --add "27:2:21:00-23:00:Description"   extra charge
```

**Charge rate:** THB 1,030.93/hr (designed so hotel's 3% WHT deduction leaves THB 1,000/hr net)

**March 2026 hours:**
- Sun-Wed: 3 hours → THB 3,092.78/day
- Thu-Sat: 2 hours → THB 2,061.86/day

**Invoice sequence:** #3026+ (separate from NOBU #3701+)
**Customer:** TCC Hotel Asset Management Co., Ltd. (Branch 00008)
**Customer address:** 199 Soi Sukhumvit 22, Sukhumvit Rd., Khlongtan, Khongtoei, Bangkok 10110
**Customer Tax ID:** 0105549106859

**WHT Form Templates (5 shared with NOBU/CRU):**
benji, ufo, linze, scotty, pound

**Sister projects:**
- NOBU/Le Du Kaan at `../NOBU/payments/` — same Bright Ears company, different rates & customer
- CRU/Cocoa XO at `../CRU/payments/` — same template layout, different rates & customer
