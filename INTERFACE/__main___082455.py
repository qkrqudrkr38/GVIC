"""
[GVIC Standard Operating Procedure]
File Name: __main___082455.py
Status: RESTORED ELITE
Function: COMMAND & CONTROL
"""

import argparse

from pip._vendor.certifi import contents, where

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--contents", action="store_true")
args = parser.parse_args()

if args.contents:
    print(contents())
else:
    print(where())
