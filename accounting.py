#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
positionen = []
dateiname = "filename.csv"

with open(dateiname) as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    for position in reader:
        positionen.append(position)

def total(positionen):
    return reduce(lambda summe, position: summe + float(position['Betrag']), positionen, 0.0)
