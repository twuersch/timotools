#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load and drop into REPL:

python -i accounting.py
ipython -i accounting.py
"""

import csv

def readCSV(filename):
    """
    Reads the given CSV file into a twodimensional list, rows first, columns second.
    """
    positionen = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for position in reader:
            positionen.append(position)
    return positionen
    

def total(positionen):
    """
    Sums up the items' 'Betrag' field.
    """
    return reduce(lambda summe, position: summe + float(position['Betrag']), positionen, 0.0)


def diff_percent(v0, v1):
    """
    Returns the difference from v0 to v1 in percent.
    """
    return (float(v1)-float(v0))/float(v0)*100.0
