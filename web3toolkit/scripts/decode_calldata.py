#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: steinkirch

from utils.strings import pprint
from utils.os import load_config
from utils.web3_wrapper import Web3Wrapper


def get_data_for_connection() -> dict:
    """Prepare a dict of data for connection."""

    data = {}
    env_keys = ['PROVIDER_URL',
                'PROVIDER_TYPE', 
                'CONTRACT_ADDRESS',
                'ABI',
                'CALLDATA']
    env_vars = load_config(env_keys) 

    data['network'] = env_vars['PROVIDER_URL']
    data['provider_type'] = env_vars['PROVIDER_URL']
    data['contract_address'] = env_vars['CONTRACT_ADDRESS']
    data['calldata'] = env_vars['CALLDATA']
    data['abi'] = env_vars['ABI']  
    return data


def decode_calldata(data) -> dict:
    """Decode raw calldata, given a contract and its ABI."""
 
    w3 = Web3Wrapper(mode=data['provider_type'],
                     network=data['network'])
  
    w3.get_pair_contract(address=data['contract_address'), abi=data['abi'))
    return w3.pair_contract.decode_function_input(data['calldata'])


if __name__ == "__main__":

    data = get_data_for_connection()
    results = decode_calldata(data)
    pprint(results)
