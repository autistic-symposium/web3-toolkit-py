#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: steinkirch
#
############################################################################################
#
#   this script is used to get transfer logs through infura's api and then parse 
#   these logs to calculate the balance of a wallet for a given token.
#   
#   to run, create an .env file with the following variables:
#   RPC_PROVIDER_URL = https://mainnet.infura.io/v3/<your infura project id>
#   CHUNK_SIZE = 100000
#   NUM_ATTEMPTS = 3
#   TRANSFER_EVENT_TOPIC_HASH = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
#   TOKEN_ADDRESS = 
#   DECIMALS = 
#
############################################################################################


import os
import requests
from pathlib import Path
from decimal import Decimal
from dotenv import load_dotenv
from collections import defaultdict


def get_env():
    """Load environment variables from .env file"""

    load_dotenv()
    env_path = Path('.')/'.env'
    load_dotenv(dotenv_path=env_path)

    env_data = {}
    env_data['RPC_PROVIDER_URL'] = os.getenv("RPC_PROVIDER_URL")
    env_data['CHUNK_SIZE'] = os.getenv("CHUNK_SIZE")
    env_data['NUM_ATTEMPTS'] = os.getenv("NUM_ATTEMPTS")
    env_data['TRANSFER_EVENT_TOPIC_HASH'] = os.getenv("TRANSFER_EVENT_TOPIC_HASH")
    env_data['TOKEN_ADDRESS'] = os.getenv("TOKEN_ADDRESS")
    env_data['DECIMALS'] = os.getenv("DECIMALS")

    if not (bool(env_data['RPC_PROVIDER_URL']) or bool(env_data['CHUNK_SIZE']) or \
            bool(env_data['NUM_ATTEMPTS']) or bool(env_data['TRANSFER_EVENT_TOPIC_HASH']) or \
            bool(env_data['TOKEN_ADDRESS']) or bool(env_data['DECIMALS'])):
        raise Exception('Please add config to .env file')

    return env_data


def convert_hex_to_int(hex_string: str) -> int:
    """Convert a hex string to an integer"""

    return int(hex_string, 16)


def send_rpc_request(url, method, params=None) -> dict:
    """Send a JSON-RPC request to a given URL"""
    
    params = params or []
    data = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': 1}

    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
        if response.status_code == 200:
            return response.json()['result']
        else:
            print('Query failed: {}.'.format(response.status_code))

    except requests.exceptions.HTTPError  as e:
        print('Error querying to {0}: {1}'.format(url, e.response.text))    
    
    except KeyError:
        print('Error querying to {0}: data not valid'.format(url))


def get_logs(address: str, from_block: int, to_block: int, topic: str, url: str) -> list:
    """Get logs from a given address between two blocks"""

    # https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_getlogs
    method = 'eth_getLogs'
    print(f'loading blocks {from_block} to {to_block}')
    
    return send_rpc_request(url, method,
                    [{'address': address, 
                    'fromBlock': from_block,
                    'toBlock': to_block, 
                    'topics': [topic]
                    }])


def get_last_block_number(url: str) -> int:
    """Get the last block number"""
    
    # https://docs.infura.io/infura/networks/ethereum/json-rpc-methods/eth_blocknumber
    method = 'eth_blockNumber'
    return convert_hex_to_int(send_rpc_request(url, method))


def get_transfer_logs(env_data: dict, address: str, decimals: int, 
                            from_block=None, to_block=None, skip_chunks=False) -> list:
    """Get transfer logs from a given address between two blocks"""

    from_block = from_block or 1
    to_block = to_block or get_last_block_number(url)
    topic = env_data['TRANSFER_EVENT_TOPIC_HASH']
    url = env_data['RPC_PROVIDER_URL']

    #################################
    # retrieve event logs by chunks
    #################################
    if not skip_chunks:
        
        logs = []
        c_size = int(env_data['CHUNK_SIZE'])
        attempts = int(env_data['NUM_ATTEMPTS'])

        for block in range(from_block, to_block, c_size):
            attempt = 0
            while attempt < attempts:
                try:
                    logs += get_logs(address, hex(block), hex(block + c_size), topic, url)
                    break
                except Exception:
                    attempt += 1

    #################################
    # retrieve event logs in one go
    #################################
    else:
        logs = get_logs(address, hex(from_block), hex(to_block), topic, url)

    return logs


def ged_processed_logs(logs: list, decimals: int) -> list:
    """Process logs to get from, to and amount"""

    decimal =  Decimal('10') ** Decimal(f'-{decimals}')
    processed_logs =  defaultdict()

    try:
        for log in logs:
            processed_logs[log['transactionHash']] = {}
            processed_logs[log['transactionHash']]['blockNumber'] = log['blockNumber']
            processed_logs[log['transactionHash']]['from'] = '0x' + log['topics'][1][26:]
            processed_logs[log['transactionHash']]['to'] = '0x' + log['topics'][2][26:]
            processed_logs[log['transactionHash']]['amount'] = Decimal(convert_hex_to_int(log['data'])) * decimal
    except KeyError as e:
        print(f'Error processing logs: {e}')
        
    return processed_logs


def get_balances(transfers: list) -> list:
    """Get balances of all addresses that have received tokens"""

    balances = defaultdict(Decimal)

    for _, transfer_data in transfers.items():
        balances[transfer_data['from']] -= transfer_data['amount']
        balances[transfer_data['to']] += transfer_data['amount']

    balances = [{'address': k, 'amount': v} for k, v in balances.items() if v > Decimal('0')]
    return sorted(balances, key=lambda x: -abs(Decimal(x['amount'])))


if __name__ == '__main__':

    env_data = get_env()
    
    address = env_data['TOKEN_ADDRESS']
    decimals = env_data['DECIMALS']

    transfer_logs = get_transfer_logs(env_data, address, decimals, from_block=16801268, to_block=16807268, skip_chunks=True)
    processed_logs = ged_processed_logs(transfer_logs, decimals)
    balances = get_balances(processed_logs)

    for balance in balances:
        print(f'{balance["address"]} has {balance["amount"]} tokens')
