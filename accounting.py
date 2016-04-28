#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from decimal import Decimal

def positionen_lesen(dateiname, delimiter="\t"):
  positionen = []
  csv.register_dialect("own", delimiter=delimiter)
  with open(dateiname) as csvfile:
      reader = csv.DictReader(csvfile, dialect="own")
      for position in reader:
          positionen.append(position)
  return positionen

def total(positionen):
    return reduce(lambda summe, position: summe + Decimal(position['Betrag']), positionen, Decimal("0"))
