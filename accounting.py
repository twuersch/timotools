#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load and drop into REPL:

python -i accounting.py
ipython -i accounting.py
"""

import csv
from decimal import Decimal
import re

def readCSV(filename, delimiter="\t"):
    """
    Reads the given CSV file into a twodimensional list, rows first, columns second.
    """
    positionen = []
    csv.register_dialect("own", delimiter=delimiter)
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, dialect="own")
        for position in reader:
            positionen.append(position)
    return positionen


def total_betrag(positionen):
    """
    Sums up the items' 'Betrag' field.
    """
    return reduce(lambda summe, position: summe + Decimal(position['Betrag']), positionen, Decimal("0"))


def diff_percent(v0, v1):
    """
    Returns the difference from v0 to v1 in percent.
    """
    return (Decimal(v1)-Decimal(v0))/Decimal(v0)*Decimal("100")

def supersum(thing):
    """
    Tries to sum up what it gets, regardless of the type
    """
    if type(thing) is str:
        splitter_re = r',|\s|\n'
        split_thing = re.split(splitter_re, thing)
        return sum(map(lambda s: Decimal(s) if s is not '' else 0, split_thing))
    elif type(thing) is list:
        decimal_list = map(lambda s: Decimal(s), thing)
        return sum(decimal_list)
