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
from pprint import pformat
from os import linesep

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
        return sum(map(lambda s: Decimal(s) if s != '' else 0, split_thing))
    elif type(thing) is list:
        decimal_list = map(lambda s: Decimal(s), thing)
        return sum(decimal_list)

class BetragProzentVonBruttolohn:
    bruttolohn = Decimal()
    prozent = Decimal()

    def __init__(self, bruttolohn, prozent):
        self.bruttolohn = bruttolohn
        self.prozent = prozent

    def decimal(self):
        return self.bruttolohn * self.prozent * Decimal("0.01")

    def __repr__(self):
        return f"{self.decimal().quantize(Decimal('0.01'))} ({self.prozent}% von {self.bruttolohn})"

class ArbeitnehmerbeitraegeBerechnung:
    arbeitnehmerbeitraege = []
    
    def __init__(self, bruttolohn):
        self.arbeitnehmerbeitraege = [
            ["AHV", BetragProzentVonBruttolohn(bruttolohn, Decimal("4.35"))],
            ["IV", BetragProzentVonBruttolohn(bruttolohn, Decimal("0.7"))],
            ["EO", BetragProzentVonBruttolohn(bruttolohn, Decimal("0.25"))],
            ["ALV", BetragProzentVonBruttolohn(bruttolohn, Decimal("1.1"))],
            ["Pensionskasse", Decimal("122.85")],
            ["Nichtberufsunfall", Decimal("36.9375").quantize(Decimal('0.01'))],
            ["KTG", (Decimal("583.80") / Decimal("12") / Decimal("2")).quantize(Decimal('0.01'))],
        ]
        
    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self):
        if self.iter_index < len(self.arbeitnehmerbeitraege):
            value = self.arbeitnehmerbeitraege[self.iter_index][1]
            self.iter_index = self.iter_index + 1
            if type(value) is BetragProzentVonBruttolohn:
                return value.decimal()
            else:
                return value
        else:
            raise StopIteration
        
    def decimal(self):
        summe = Decimal()
        for zeile in self.arbeitnehmerbeitraege:
            if type(zeile[1]) is not Decimal:
                summe = summe + zeile[1].decimal()
            else:
                summe = summe + zeile[1]
        return summe

    def __repr__(self):
        return pformat(self.arbeitnehmerbeitraege) \
            + linesep \
            + "-> Total Arbeitnehmerbeiträge: " \
            + f"{self.decimal().quantize(Decimal('0.01'))}"
            
class ArbeitgeberbeitraegeBerechnung:
    arbeitgeberbeitraege = []

    def __init__(self, bruttolohn):
        self.arbeitgeberbeitraege = [
            ["AHV", BetragProzentVonBruttolohn(bruttolohn, Decimal("4.35"))],
            ["IV", BetragProzentVonBruttolohn(bruttolohn, Decimal("0.7"))],
            ["EO", BetragProzentVonBruttolohn(bruttolohn, Decimal("0.25"))],
            ["ALV", BetragProzentVonBruttolohn(bruttolohn, Decimal("1.1"))],
            ["Pensionskasse", Decimal("122.85")],
            ["FAK", BetragProzentVonBruttolohn(bruttolohn, Decimal("1.2"))],
            ["Berufsunfall", Decimal("22.8125").quantize(Decimal('0.01'))],
            ["KTG", (Decimal("583.80") / Decimal("12") / Decimal("2")).quantize(Decimal('0.01'))],
        ]

    def __iter__(self):
        self.iter_index = 0
        return self
        
    def __next__(self):
        if self.iter_index < len(self.arbeitgeberbeitraege):
            value = self.arbeitgeberbeitraege[self.iter_index][1]
            self.iter_index = self.iter_index + 1
            if type(value) is BetragProzentVonBruttolohn:
                return value.decimal()
            else:
                return value
        else:
            raise StopIteration
        
    def decimal(self):
        summe = Decimal()
        for zeile in self.arbeitgeberbeitraege:
            if type(zeile[1]) is not Decimal:
                summe = summe + zeile[1].decimal()
            else:
                summe = summe + zeile[1]
        return summe

    def __repr__(self):
        return pformat(self.arbeitgeberbeitraege) \
            + linesep \
            + "-> Total Arbeitgeberbeiträge: " \
            + f"{self.decimal().quantize(Decimal('0.01'))}"

bruttolohn = Decimal(3500)
agberechnung = ArbeitgeberbeitraegeBerechnung(bruttolohn)
anberechnung = ArbeitnehmerbeitraegeBerechnung(bruttolohn)
nettolohn = bruttolohn - anberechnung.decimal()
totalkosten = bruttolohn + agberechnung.decimal()
