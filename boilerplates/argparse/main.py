#!/usr/bin/env python

import argparse


def main():

    description = 'Describe what your app does here'

    # Run CLI menu.
    parser = argparse.ArgumentParser(description=description)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-e', '--encode', type=int, help="some help here")

    group.add_argument('-d', '--decode', help="another help here")

    args = parser.parse_args()

    print(args.encode)
    print(args.decode)


if __name__ == "__main__":
    main()
