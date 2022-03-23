# -*- coding: utf8 -*-

import os
import sys
import logging as l

from src.settings import BOUNDARY_LIMIT_ENC, BOUNDARY_LIMIT_DEC


def parse_input_stream(filename):
    """
    Loads a file with the input stream with
    encoded commands.
    
    Returns:
        filename -- location of the file in disk.
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()

            for input_stream in lines:
                if input_stream[0] != '#':
                    l.debug('Input stream:\n{}'.format(input_stream))
                    return input_stream.strip()

    except (KeyError, OSError, TypeError) as e:
        l.error('Could not open input stream file {0}: {1}.'.format(filename, e))
        sys.exit(0)


def get_boundary_limits(lim_base):
    """
    Extract boundary limits from env file, returning two integers
    representing these limits, either in the encoded or
    the decode base.

    Arguments:
        lim_base {string}: 'enc' for the encoded limit 
            representation or 'dec' for the encoded limit
            representation.
    """
    try:
        if lim_base == 'enc':
            enc_range = tuple(BOUNDARY_LIMIT_ENC.split(', '))
            return int(enc_range[0]), int(enc_range[1])
        
        elif lim_base == 'dec':
            dec_range = tuple(BOUNDARY_LIMIT_DEC.split(', '))
            return int(dec_range[0], 16), int(dec_range[1], 16)

    except (KeyError, ValueError, AttributeError) as e:
        l.error('Could not extract boundary limits from .env file: {}'.format(e))
        return -1