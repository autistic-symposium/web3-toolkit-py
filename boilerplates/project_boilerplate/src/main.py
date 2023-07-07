#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# src/main.py

import argparse


def run_menu() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description='Run my project')

    parser.add_argument('-t', dest='test', nargs=1,
                        help="Run test method. \
                        Example: <my project> -t <argument>")

    return parser


def run() -> None:
    """Entry point for this module."""

    parser = run_menu()
    args = parser.parse_args()

    if args.test:
        pass

    else:
        parser.print_help()


if __name__ == "__main__":
    run()
