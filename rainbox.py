#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ressources.tools as t
import argparse
import multiprocessing as mp
import sys

######################################
######################################


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def parsing():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description="""
                            ██████╗  █████╗ ██╗███╗   ██╗██████╗  ██████╗ ██╗  ██╗
                            ██╔══██╗██╔══██╗██║████╗  ██║██╔══██╗██╔═══██╗╚██╗██╔╝
                            ██████╔╝███████║██║██╔██╗ ██║██████╔╝██║   ██║ ╚███╔╝ 
                            ██╔══██╗██╔══██║██║██║╚██╗██║██╔══██╗██║   ██║ ██╔██╗ 
                            ██║  ██║██║  ██║██║██║ ╚████║██████╔╝╚██████╔╝██╔╝ ██╗
                            ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
                                     A generator of wifi router keys
                                             Author: n3rada
        """,
    )

    # nargs='?' because it's not obligatory
    parser.add_argument(
        "-c",
        "--cores",
        type=int,
        nargs="?",
        default=mp.cpu_count(),
        help="Number of cores to use",
    )

    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="hexa",
        help="Alphabet type: hexa or alpha (for all)",
    )

    parser.add_argument(
        "-a", "--alphabet", type=str, default=None, help="Alphabet case: low, up or mix"
    )

    parser.add_argument("-l", "--length", type=int, default=None, help="Ouput key size")

    parser.add_argument(
        "-w", "--wordlist", action="store_true", help="Wordlist output activated."
    )

    parser.add_argument(
        "-p",
        "--punctuation",
        action="store_true",
        help="Add punctuation to generation.",
    )

    parser.add_argument(
        "-tf",
        "--toFind",
        type=str,
        default=False,
        nargs="?",
        help="Enter the key to find here for testing the generator. Cannot be combined with wordlist !",
    )

    # If no arguments have been passed
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        return parser.parse_args()


def main():

    args = parsing()

    try:
        fragmentName = (
            "FRAG_4_"
            + args.type.upper()
            + "-"
            + args.alphabet
            + "-"
            + str(args.punctuation)
        )
    except TypeError:
        fragmentName = None

    t.clear(withAscii=True)

    try:
        t.writer(
            keySize=args.length,
            cores=args.cores,
            fragName=fragmentName,
            wordlist=args.wordlist,
            keyToFind=args.toFind,
        )
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
