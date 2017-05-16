#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set Tool: Line-by-line text file union, intersection, difference etc.
Timo Würsch July 2013
"""

def textfile_to_set(filename, tolower):
    lines_as_set = set()
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if tolower:
                line = line.lower()
            if line != "":
                lines_as_set.add(line)
    return lines_as_set

if __name__ == '__main__':
    # Parse command line arguments
    import argparse, sys
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("-i", "--insensitive", help = "Make matching case insensitive. Default is case-sensitive.", action = "store_true")
    argument_parser.add_argument("fileA", help = "File with the elements for set A")
    argument_parser.add_argument("op", help = "Operator. One of: union (u, +), intersect (n, i), difference (d, -), equals (equal, is, =), strictsuperset (>, strictsuper), superset (>=, super), strictsubset (<, strictsub), subset (<=, sub)")
    argument_parser.add_argument("fileB", help = "File with the elements for set B")
    args = argument_parser.parse_args()
    if args.op.lower() in ["u", "union", "+"]:
        operator = "union"
    elif args.op.lower() in ["i", "intersect", "intersection", "n"]:
        operator = "intersection"
    elif args.op.lower() in ["d", "diff", "difference", "-"]:
        operator = "difference"
    elif args.op.lower() in ["equals", "equal", "is", "="]:
        operator = "equality"
    elif args.op.lower() in [">", "strictsuperset", "strictsuper"]:
        operator = "strictsuperset"
    elif args.op.lower() in [">=", "superset", "super"]:
        operator = "superset"
    elif args.op.lower() in ["<", "strictsubset", "strictsub"]:
        operator = "strictsubset"
    elif args.op.lower() in ["<=", "subset", "sub"]:
        operator = "subset"
    elif args.op.lower() in ["disjoint", "dis"]:
        operator = "disjoint"
    else:
        print("Unknown operator \"" + args.op + "\".")
        argument_parser.print_help()
        sys.exit(1)
    
    # Read files
    try:
        setA = textfile_to_set(args.fileA, args.insensitive)
    except IOError:
        print("Could not open file A \"" + args.fileA + "\"")
        sys.exit(1)
    try:
        setB = textfile_to_set(args.fileB, args.insensitive)
    except IOError:
        print("Could not open file B \"" + args.fileB + "\"")
        sys.exit(1)    
    
    # Calculate
    if operator == "union":
        result = setA.union(setB)
    elif operator == "intersection":
        result = setA.intersection(setB)
    elif operator == "difference":
        result = setA.difference(setB)
    elif operator == "equality":
        result = setA == setB
    elif operator == "strictsuperset":
        result = setA > setB
    elif operator == "superset":
        result = setA >= setB
    elif operator == "strictsubset":
        result = setA < setB
    elif operator == "subset":
        result = setA <= setB
    elif operator == "disjoint":
        result = setA.isdisjoint(setB)
    
    # Output
    if type(result) == set:
        for element in result:
            print(element)
    elif type(result) == bool:
        if result:
            print(str(True))
        else:
            print(str(False))
    
    # That's all folks!
    sys.exit(0)
