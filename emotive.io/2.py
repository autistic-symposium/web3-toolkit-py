#!/usr/bin/env python3

import sys
from pprint import pprint
from pymongo import MongoClient


class AWS_fail(object):
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.aws_fail

    def print_collection(self):
        ''' Print the entire items collection. Debug purposes.'''
        for item in self.db.items.find():
            pprint(item)

    def item_exists(self, sku):
        ''' Check whether a given sku entry exists in the collection.'''
        return self.db.items.find_one({'sku_number': sku})

    def add_item_db(self, sku):
        ''' Add a new sku to the collection or increment its value.'''
        if not self.item_exists(sku):
            self.db.items.insert_one({'sku_number': sku, 'quantity': 1})
        else:
           self.db.items.update_one({'sku_number': sku}, {'$inc': {'quantity': 1}})

    def rm_item_db(self, sku):
        ''' Remove a sku item from the database.'''
        if self.item_exists(sku):
            self.db.items.delete_one({'sku_number': sku})

    def check_quantity_count(self, z):
        ''' Check whether the sku item has the given z quantity.'''
        z_found = self.db.items.find_one({'quantity': int(z)})
        if z_found:
            pprint(1)
        else:
            pprint(0)
    
    def cleanup(self):
        self.db.items.drop()


def load_input(filename):
    ''' Load input file with list of db operations.'''
    try:
        with open(filename) as f:
            input_data = f.readlines()
            return input_data[0], input_data[1:]
    except IOError:
        pprint('Could not read file: {}. Exiting.').format(f)
        sys.exit(1)


def run_operation(operation, aws_fail):
    ''' Run the db operations for the given db collection.'''
    if operation[0] == '1':
        aws_fail.add_item_db(operation[1])
    elif operation[0] == '2':
        aws_fail.rm_item_db(operation[1])
    elif operation[0] == '3':
        aws_fail.check_quantity_count(operation[1])


if __name__ == "__main__":

    aws_fail = AWS_fail()

    filename = 'input_for_2.txt'
    num_operations, operation_list = load_input(filename)

    # We could use len(operation_list) here, but let's use the input info
    # because len() is not optimized for a large number of operations
    for i in range(int(num_operations)):
        operation = operation_list[i].strip('\n').split(',')
        run_operation(operation, aws_fail)
    
    aws_fail.cleanup()
    