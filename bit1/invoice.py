"""
Command-line tool to print a formatted invoice based on a
worker's timesheet.  The worker information must be provided
in a JSON file and the timesheet as a CSV file.
Run the tool to see usage info.
"""

import sys
import json
from decimal import Decimal


def load_worker(worker_fn):
    """
    Load worker information from a JSON file and return as
    a Python dictionary.
    """
    return json.load(open(worker_fn))


def load_timesheet(timesheet_fn):
    """
    A Python generator to oad a timesheet from a CSV file
    and yield hours worked for each day.
    """
    for line in open(timesheet_fn):
        _date_str, hours_str = line.split(', ')
        yield Decimal(hours_str)


def generate_invoice_data(worker, timesheet):
    " Return invoice data for the given worker and timesheet "
    total_hours = sum(timesheet)
    invoice = {
        'worker': worker,
        'hours': total_hours,
        'amount': total_hours * Decimal(worker['rate'])}
    return invoice


def format_invoice(inv):
    " Take invoice data (inv) and return as formatted text. "
    service = inv['worker']['service']
    return f"""
Worker: {inv['worker']['name']}

Item                    | Quantity      | Total
{service:>16} \t| {inv['hours']:>5} \t| {inv['amount']:>5}

Payment information:
    {inv['worker']['payment_info']['sort-code']}
    {inv['worker']['payment_info']['account']}

Thank you!
"""


def create_invoice(worker_fn, timesheet_fn):
    """
    Create a nicely formatted invoice based on the worker
    information and timesheet data in the provided files.
    """
    worker = load_worker(worker_fn)
    timesheet = load_timesheet(timesheet_fn)
    invoice = generate_invoice_data(worker, timesheet)
    return format_invoice(invoice)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: invoce.py WORKER TIMESHEET")
        exit()
    print(create_invoice(sys.argv[1], sys.argv[2]))
