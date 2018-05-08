#!/usr/bin/env python3
"""adapted from https://github.com/kindlychung/translator"""
from translator import Translator

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser("Translate a file")
    parser.add_argument("--fromlang", "-f", default="nl", help="From language, default to nl")
    parser.add_argument("--tolang", "-t", default="en", help="To language, default to en")
    parser.add_argument("--inputfile", "-i", help="Input file, default to stdin")
    parser.add_argument("--outputfile", "-o", help="Output file, default to stdout")
    args = parser.parse_args()

    if not args.inputfile:
        print('type a text to translate')
        input_string = input()
    else:
        with open(args.inputfile, encoding="utf8", errors="replace") as fh:

            input_string = fh.read()

    trans = Translator(args.fromlang, args.tolang, input_string)
    t = trans.translate(verbose=True)
    #print(t)
    #output_string = trans.prettify()

    if not args.outputfile:
        print(t)
    else:
        with open(args.outputfile, "w", encoding="utf8", errors="replace") as fh:
            fh.write(t)


if __name__ == "__main__":
    main()
