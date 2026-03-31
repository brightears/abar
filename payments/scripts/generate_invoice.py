#!/usr/bin/env python3
"""
Generate monthly invoice for Bright Ears DJ services at ABar.
Single venue — no --venue flag needed.
Supports variable hours per day of week (e.g., 3hr Sun-Wed, 2hr Thu-Sat).

Usage: python generate_invoice.py YYYY-MM [options]
"""

import argparse
import json
import re
import subprocess
import sys
from calendar import monthrange
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
from string import Template

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOURLY_RATE = Decimal('1030.93')  # THB per hour (incorporates 3% WHT)
DEFAULT_HOURS = 3                 # Default hours per day
VAT_RATE = Decimal('0.07')
WHT_RATE = Decimal('0.03')

VENUE = {
    'description': 'ABar DJ Service',
    'time_3hr': '21:00 - 24:00',
    'time_2hr': '22:00 - 24:00',
    'label': 'ABar',
    'file_tag': 'abar',
}

CUSTOMER = {
    'name': 'TCC Hotel Asset Management Co., Ltd. (Branch 00008)',
    'address': '199 Soi Sukhumvit 22, Sukhumvit Rd., Khlongtan, Khongtoei',
    'city': 'Bangkok 10110, Thailand',
    'tax_id': '0105549106859',
}

TAX_NO = '0105550096659'  # Bright Ears tax number

MONTH_NAMES = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

MONTH_FULL = ['', 'January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# Day of week abbreviations (Monday=0 ... Sunday=6)
DAY_ABBREVS = {
    'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6,
}

# ---------------------------------------------------------------------------
# Number to words
# ---------------------------------------------------------------------------

ONES = ['', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN',
        'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE', 'THIRTEEN',
        'FOURTEEN', 'FIFTEEN', 'SIXTEEN', 'SEVENTEEN', 'EIGHTEEN', 'NINETEEN']
TENS = ['', '', 'TWENTY', 'THIRTY', 'FORTY', 'FIFTY',
        'SIXTY', 'SEVENTY', 'EIGHTY', 'NINETY']


def number_to_words(n):
    """Convert integer to English words (up to 999,999)."""
    if n == 0:
        return 'ZERO'
    if n < 20:
        return ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return TENS[tens] + ('-' + ONES[ones] if ones else '')
    if n < 1000:
        hundreds, remainder = divmod(n, 100)
        return ONES[hundreds] + ' HUNDRED' + (' ' + number_to_words(remainder) if remainder else '')
    if n < 1000000:
        thousands, remainder = divmod(n, 1000)
        return number_to_words(thousands) + ' THOUSAND' + (' ' + number_to_words(remainder) if remainder else '')
    return str(n)


def amount_to_words(amount):
    """Convert decimal amount to English words for invoice."""
    amount_str = f"{amount:.2f}"
    integer_part, decimal_part = amount_str.split('.')

    words = number_to_words(int(integer_part))

    cents = int(decimal_part)
    if cents > 0:
        words += ' POINT ' + number_to_words(cents)

    return words + ' BAHT'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def ordinal(n):
    """Return ordinal suffix: 1->st, 2->nd, 3->rd, else->th."""
    if 11 <= n % 100 <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')


def format_date_range(year, month):
    """Format as DD.MM.YY - DD.MM.YY for base charge line."""
    days = monthrange(year, month)[1]
    yy = str(year)[-2:]
    return f"01.{month:02d}.{yy} - {days:02d}.{month:02d}.{yy}"


def format_date_single(year, month, day):
    """Format as DD.MM.YYYY for adjustment lines."""
    return f"{day:02d}.{month:02d}.{year}"


def fmt(amount):
    """Format Decimal amount for display: 3,711.34 THB"""
    return f"{amount:,.2f} THB"


def get_day_of_week(year, month, day):
    """Return day of week (0=Monday ... 6=Sunday)."""
    return date(year, month, day).weekday()


def get_hours_for_day(year, month, day, short_days):
    """Return hours for a specific day based on short_days config."""
    if short_days and get_day_of_week(year, month, day) in short_days:
        return 2
    return DEFAULT_HOURS


def count_days_by_hours(year, month, short_days, no_days=None):
    """Count 3-hour days and 2-hour days in a month."""
    days_in_month = monthrange(year, month)[1]
    excluded = set(no_days or [])
    three_hr = 0
    two_hr = 0
    for d in range(1, days_in_month + 1):
        if d in excluded:
            continue
        hours = get_hours_for_day(year, month, d, short_days)
        if hours == 3:
            three_hr += 1
        else:
            two_hr += 1
    return three_hr, two_hr


# ---------------------------------------------------------------------------
# Line item builder
# ---------------------------------------------------------------------------

def build_line_items(year, month, short_days=None, no_days=None,
                     credits=None, additions=None):
    """Build invoice line items.

    Args:
        year, month: invoice period
        short_days: set of weekday numbers (0=Mon..6=Sun) with 2-hour sets
        no_days: list of day numbers where no service was provided
        credits: list of dicts {'day': int, 'hours': int, 'description': str}
        additions: list of dicts {'day': int, 'hours': int, 'time': str, 'description': str}

    Returns: list of line item dicts
    """
    days_in_month = monthrange(year, month)[1]
    month_abbr = MONTH_NAMES[month]

    items = []
    line_no = 1

    # Calculate base charge with variable hours
    three_hr_days, two_hr_days = count_days_by_hours(year, month, short_days, no_days)

    if two_hr_days == 0:
        # All days are 3-hour — single line item
        base_amount = HOURLY_RATE * 3 * (three_hr_days + two_hr_days)
        active_days = three_hr_days
        items.append({
            'no': line_no,
            'description': f'{VENUE["description"]} ({active_days} days × 3 hrs)',
            'date': format_date_range(year, month),
            'time': VENUE['time_3hr'],
            'price': HOURLY_RATE * 3,
            'amount': base_amount,
        })
        line_no += 1
    else:
        # Split into 3-hour and 2-hour line items
        if three_hr_days > 0:
            amount_3hr = HOURLY_RATE * 3 * three_hr_days
            items.append({
                'no': line_no,
                'description': f'{VENUE["description"]} ({three_hr_days} days × 3 hrs)',
                'date': format_date_range(year, month),
                'time': VENUE['time_3hr'],
                'price': HOURLY_RATE * 3,
                'amount': amount_3hr,
            })
            line_no += 1

        if two_hr_days > 0:
            amount_2hr = HOURLY_RATE * 2 * two_hr_days
            items.append({
                'no': line_no,
                'description': f'{VENUE["description"]} ({two_hr_days} days × 2 hrs)',
                'date': format_date_range(year, month),
                'time': VENUE['time_2hr'],
                'price': HOURLY_RATE * 2,
                'amount': amount_2hr,
            })
            line_no += 1

    # Deductions for cancelled days (full day no-shows already excluded from base)
    # No need to subtract — they're already excluded from the count above.
    # But we do list them for transparency:
    if no_days:
        for day in sorted(no_days):
            hours = get_hours_for_day(year, month, day, short_days)
            # These are already NOT counted in the base, so we just add a note line
            # Actually, let's handle this differently:
            # Re-include them in base and subtract here for clarity
            pass

    # Credits — partial hour deductions on otherwise full days (e.g., DJ late arrival)
    if credits:
        for cr in credits:
            day = cr['day']
            hours = cr['hours']
            credit_amount = (HOURLY_RATE * hours).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            desc = cr.get('description') or f'Credit: {hours}hr on {month_abbr} {day}<sup>{ordinal(day)}</sup>'
            items.append({
                'no': line_no,
                'description': desc,
                'date': format_date_single(year, month, day),
                'time': '-',
                'price': -credit_amount,
                'amount': -credit_amount,
            })
            line_no += 1

    # Additions — extra charges (e.g., additional DJ hours)
    if additions:
        for add in additions:
            day = add['day']
            hours = add['hours']
            time_range = add.get('time', '-')
            add_amount = (HOURLY_RATE * hours).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            desc = add['description']
            items.append({
                'no': line_no,
                'description': desc,
                'date': format_date_single(year, month, day),
                'time': time_range,
                'price': add_amount,
                'amount': add_amount,
            })
            line_no += 1

    return items


def build_line_items_alt(year, month, short_days=None, no_days=None,
                         credits=None, additions=None):
    """Alternative: include all days in base, then subtract cancelled days.
    This matches the NOBU invoice style more closely."""
    days_in_month = monthrange(year, month)[1]
    month_abbr = MONTH_NAMES[month]

    items = []
    line_no = 1

    # Base charge: ALL days (including those that will be cancelled)
    three_hr_all, two_hr_all = count_days_by_hours(year, month, short_days, no_days=None)

    if two_hr_all == 0:
        base_amount = HOURLY_RATE * 3 * days_in_month
        items.append({
            'no': line_no,
            'description': f'{VENUE["description"]} ({days_in_month} days × 3 hrs)',
            'date': format_date_range(year, month),
            'time': VENUE['time_3hr'],
            'price': HOURLY_RATE * 3,
            'amount': base_amount,
        })
        line_no += 1
    else:
        if three_hr_all > 0:
            amount_3hr = HOURLY_RATE * 3 * three_hr_all
            items.append({
                'no': line_no,
                'description': f'{VENUE["description"]} ({three_hr_all} days × 3 hrs)',
                'date': format_date_range(year, month),
                'time': VENUE['time_3hr'],
                'price': HOURLY_RATE * 3,
                'amount': amount_3hr,
            })
            line_no += 1
        if two_hr_all > 0:
            amount_2hr = HOURLY_RATE * 2 * two_hr_all
            items.append({
                'no': line_no,
                'description': f'{VENUE["description"]} ({two_hr_all} days × 2 hrs)',
                'date': format_date_range(year, month),
                'time': VENUE['time_2hr'],
                'price': HOURLY_RATE * 2,
                'amount': amount_2hr,
            })
            line_no += 1

    # Deductions for cancelled days
    if no_days:
        for day in sorted(no_days):
            hours = get_hours_for_day(year, month, day, short_days)
            deduction = HOURLY_RATE * hours
            items.append({
                'no': line_no,
                'description': f'No DJ Service on {month_abbr} {day}<sup>{ordinal(day)}</sup>',
                'date': format_date_single(year, month, day),
                'time': '-',
                'price': -deduction,
                'amount': -deduction,
            })
            line_no += 1

    # Credits
    if credits:
        for cr in credits:
            day = cr['day']
            hours = cr['hours']
            credit_amount = (HOURLY_RATE * hours).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            desc = cr.get('description') or f'Credit: {hours}hr on {month_abbr} {day}<sup>{ordinal(day)}</sup>'
            items.append({
                'no': line_no,
                'description': desc,
                'date': format_date_single(year, month, day),
                'time': '-',
                'price': -credit_amount,
                'amount': -credit_amount,
            })
            line_no += 1

    # Additions
    if additions:
        for add in additions:
            day = add['day']
            hours = add['hours']
            time_range = add.get('time', '-')
            add_amount = (HOURLY_RATE * hours).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            desc = add['description']
            items.append({
                'no': line_no,
                'description': desc,
                'date': format_date_single(year, month, day),
                'time': time_range,
                'price': add_amount,
                'amount': add_amount,
            })
            line_no += 1

    return items


def build_line_items_html(items):
    """Convert line items to HTML table rows."""
    rows = []
    for item in items:
        price_str = fmt(item['price'])
        amount_str = fmt(item['amount'])
        rows.append(f"""    <tr>
      <td class="col-no">{item['no']}</td>
      <td class="col-desc">{item['description']}</td>
      <td class="col-date">{item['date']}</td>
      <td class="col-time">{item['time']}</td>
      <td class="col-price">{price_str}</td>
      <td class="col-amount">{amount_str}</td>
    </tr>""")
    return '\n'.join(rows)


# ---------------------------------------------------------------------------
# Invoice config (number tracking)
# ---------------------------------------------------------------------------

def get_config_path():
    return Path(__file__).parent.parent / 'invoice_config.json'


def get_next_invoice_no():
    config_path = get_config_path()
    if config_path.exists():
        config = json.loads(config_path.read_text())
        return config['last_invoice_no'] + 1
    return None


def save_invoice_no(invoice_no, month_str):
    config_path = get_config_path()
    config = {'last_invoice_no': invoice_no, 'last_invoice_month': month_str}
    config_path.write_text(json.dumps(config, indent=2) + '\n')


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

def generate_pdf(html_path, pdf_path):
    """Convert HTML to PDF using Chrome headless."""
    cmd = [
        CHROME,
        '--headless=new',
        '--disable-gpu',
        f'--print-to-pdf={pdf_path}',
        '--print-to-pdf-no-header',
        f'file://{html_path}',
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Warning: PDF generation may have issues: {result.stderr[:200]}")
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_short_days(short_days_str):
    """Parse comma-separated day abbreviations into set of weekday numbers.
    Example: 'thu,fri,sat' -> {3, 4, 5}
    """
    if not short_days_str:
        return None
    days = set()
    for d in short_days_str.lower().split(','):
        d = d.strip()
        if d in DAY_ABBREVS:
            days.add(DAY_ABBREVS[d])
        else:
            print(f"Warning: Unknown day abbreviation '{d}'. Use: mon,tue,wed,thu,fri,sat,sun")
    return days if days else None


def parse_credit_arg(credit_str):
    """Parse --credit argument: 'DAY:HOURS:Description text' -> dict"""
    parts = credit_str.split(':', 2)
    if len(parts) < 2:
        print(f"Error: Invalid --credit format: {credit_str}")
        print("Expected: DAY:HOURS[:DESCRIPTION] (e.g., 18:1:Late arrival)")
        sys.exit(1)

    day = int(parts[0])
    hours = int(parts[1])
    description = parts[2] if len(parts) > 2 else None

    return {'day': day, 'hours': hours, 'description': description}


def parse_add_arg(add_str):
    """Parse --add argument: 'DAY:HOURS:START-END:Description text' -> dict"""
    parts = add_str.split(':', 3)
    if len(parts) < 4:
        print(f"Error: Invalid --add format: {add_str}")
        print("Expected: DAY:HOURS:START-END:DESCRIPTION")
        print("  e.g., 15:2:21:00-23:00:Extra DJ for private event")
        sys.exit(1)

    day = int(parts[0])
    hours = int(parts[1])
    remainder = ':'.join(parts[2:])
    time_match = re.match(r'(\d+:\d+\s*-\s*\d+:\d+):(.*)', remainder)
    if time_match:
        time_range = time_match.group(1).replace('-', ' - ').replace('  ', ' ')
        description = time_match.group(2)
    else:
        time_range = '-'
        description = remainder

    return {'day': day, 'hours': hours, 'time': time_range, 'description': description}


def parse_args():
    parser = argparse.ArgumentParser(description='Generate Bright Ears monthly invoice for ABar')
    parser.add_argument('month', help='Invoice month (YYYY-MM)')
    parser.add_argument('--short-days', help='Days of week with 2hr sets (e.g., thu,fri,sat)')
    parser.add_argument('--invoice-no', type=int, help='Invoice number (auto-increments if omitted)')
    parser.add_argument('--date', help='Invoice date (DD.MM.YYYY, defaults to today)')
    parser.add_argument('--no-day', action='append', type=int, help='Day with no service (e.g., --no-day 15)')
    parser.add_argument('--credit', action='append', help='Hour credit: DAY:HOURS[:DESCRIPTION]')
    parser.add_argument('--add', action='append', help='Additional charge: DAY:HOURS:START-END:DESCRIPTION')
    parser.add_argument('--html-only', action='store_true', help='Skip PDF generation')
    parser.add_argument('--dry-run', action='store_true', help='Preview calculations only')
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    year, month = map(int, args.month.split('-'))
    month_str = f"{year}-{month:02d}"
    short_days = parse_short_days(args.short_days)

    # 1. Invoice number
    if args.invoice_no:
        invoice_no = args.invoice_no
    else:
        invoice_no = get_next_invoice_no()
        if invoice_no is None:
            print("Error: No previous invoice found. Use --invoice-no to set the first number.")
            sys.exit(1)

    # 2. Collect cancelled days
    no_days = args.no_day or []
    if no_days:
        print(f"Cancelled days: {sorted(no_days)}")

    # 3. Parse adjustments
    credits = [parse_credit_arg(c) for c in args.credit] if args.credit else None
    additions = [parse_add_arg(a) for a in args.add] if args.add else None

    # 4. Show hours breakdown
    three_hr, two_hr = count_days_by_hours(year, month, short_days, no_days or None)
    if short_days:
        day_names = {v: k for k, v in DAY_ABBREVS.items()}
        short_list = ', '.join(day_names[d].capitalize() for d in sorted(short_days))
        print(f"Short days (2hr): {short_list}")
        print(f"3-hour days: {three_hr}, 2-hour days: {two_hr}")

    # 5. Build line items (use alt style: include all, then deduct)
    items = build_line_items_alt(year, month, short_days, no_days or None,
                                 credits, additions)

    # 6. Calculate totals
    sub_total = sum(item['amount'] for item in items)
    vat = (sub_total * VAT_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    grand_total = sub_total + vat
    wht = (sub_total * WHT_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    net_amount = grand_total - wht

    # 7. Print summary
    print(f"\n{'='*50}")
    print(f"Invoice #{invoice_no} — {VENUE['label']} — {MONTH_FULL[month]} {year}")
    print(f"{'='*50}")
    print(f"\nLine items:")
    for item in items:
        desc = re.sub(r'<[^>]+>', '', item['description']).replace('&amp;', '&')
        print(f"  {item['no']:>2}. {desc:<45} {item['amount']:>12,.2f}")
    print(f"\n  {'Sub Total:':<47} {sub_total:>12,.2f} THB")
    print(f"  {'VAT 7%:':<47} {vat:>12,.2f} THB")
    print(f"  {'Grand Total:':<47} {grand_total:>12,.2f} THB")
    print(f"  {'WHT 3%:':<47} {-wht:>12,.2f} THB")
    print(f"  {'Net Amount:':<47} {net_amount:>12,.2f} THB")
    print(f"\n  Written: {amount_to_words(net_amount)}")

    if args.dry_run:
        print("\n[Dry run — no files generated]")
        return

    # 8. Load template and generate HTML
    template_path = Path(__file__).parent.parent / 'templates' / 'invoice-template.html'
    template = Template(template_path.read_text())

    invoice_date = args.date or date.today().strftime('%d.%m.%Y')

    html = template.safe_substitute(
        INVOICE_NO=f'# {invoice_no}',
        INVOICE_DATE=invoice_date,
        TAX_NO=TAX_NO,
        CUSTOMER_NAME=CUSTOMER['name'],
        CUSTOMER_ADDRESS=CUSTOMER['address'],
        CUSTOMER_CITY=CUSTOMER['city'],
        CUSTOMER_TAX_ID=CUSTOMER['tax_id'],
        LINE_ITEMS_HTML=build_line_items_html(items),
        SUB_TOTAL=fmt(sub_total),
        VAT_AMOUNT=fmt(vat),
        GRAND_TOTAL=fmt(grand_total),
        WHT_AMOUNT=fmt(-wht),
        NET_AMOUNT=fmt(net_amount),
        WRITTEN_AMOUNT=amount_to_words(net_amount),
    )

    # 9. Write output
    output_dir = Path(__file__).parent.parent / month_str
    output_dir.mkdir(exist_ok=True)

    month_abbr = MONTH_NAMES[month].lower()
    filename_base = f"invoice-{invoice_no}-abar-{month_abbr}{year}"

    html_path = output_dir / f"{filename_base}.html"
    html_path.write_text(html)
    print(f"\nHTML: {html_path}")

    # 10. Generate PDF
    if not args.html_only:
        pdf_path = output_dir / f"{filename_base}.pdf"
        print(f"Generating PDF...")
        generate_pdf(str(html_path.resolve()), str(pdf_path.resolve()))
        print(f"PDF:  {pdf_path}")

    # 11. Update invoice counter
    save_invoice_no(invoice_no, month_str)
    print(f"\nInvoice #{invoice_no} (ABar) generated successfully.")


if __name__ == '__main__':
    main()
