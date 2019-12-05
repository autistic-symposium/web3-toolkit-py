#!/usr/bin/env python3

import os
import re
import click


@click.command()

@click.option('-s', 
            '--source', 
            default='dev', 
            nargs=1, 
            show_default=True, 
            help='Some source string.')

@click.option('-t', 
            '--target', 
            default='staging', 
            nargs=1, 
            show_default=True, 
            help='Some target string.')

@click.option('-p', 
            '--services', 
            required=True)


def main(source, target, services):
    print(source, target, services)


if __name__ == "__main__":
    main(source, target, services)
