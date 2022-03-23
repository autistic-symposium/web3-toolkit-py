#!/usr/bin/env python

import logging as l

import src.Epen as Epen
import src.utils as utils

from src.settings import LOG_LEVEL, LOG_FORMAT, INPUT_STREAM_FILE

# Define log level: choose between DEBUG or INFO.
l.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)


def main():

    p = Epen.EPen()

    # Get input stream from file.
    input_stream = utils.parse_input_stream(INPUT_STREAM_FILE)

    # Extract and run list of commands from stream input.
    if input_stream:
        p.parse_stream(input_stream)


if __name__ == "__main__":
    main()
    
