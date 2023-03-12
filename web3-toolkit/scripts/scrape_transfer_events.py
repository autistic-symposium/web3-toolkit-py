#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# author: steinkirch
#
############################################################################################
#
#   this script is used to scrape transfer logs through events topics.
#   
#   to run, create an .env file with the following variables:
#   RPC_PROVIDER_URL = https://mainnet.infura.io/v3/<your infura project id>
#   CHUNK_SIZE = 10000
#   TRANSFER_EVENT_TOPIC_HASH = 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
#   TOKEN_ADDRESS = 
#   SLEEP_TIME = 0.005 
#
############################################################################################


import os
from time import sleep
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv


def get_env():
    """Load environment variables from .env file"""

    load_dotenv()
    env_path = Path('..')/'.env'
    load_dotenv(dotenv_path=env_path)

    env_data = {}
    env_data['RPC_PROVIDER_URL'] = os.getenv("RPC_PROVIDER_URL")
    env_data['CHUNK_SIZE'] = os.getenv("CHUNK_SIZE")
    env_data['TOKEN_ADDRESS'] = os.getenv("TOKEN_ADDRESS")
    env_data['TRANSFER_EVENT_TOPIC_HASH'] = os.getenv("TRANSFER_EVENT_TOPIC_HASH")
    env_data['SLEEP_TIME'] = os.getenv("SLEEP_TIME")

    if not (bool(env_data['RPC_PROVIDER_URL']) or bool(env_data['CHUNK_SIZE']) or \
           bool(env_data['SLEEP_TIME']) or bool(env_data['TOKEN_ADDRESS']) or \
           bool(env_data['TRANSFER_EVENT_TOPIC_HASH'])):
        raise Exception('Please add config to .env file')

    return env_data


def create_web3_connection(url):
    """Create a web3 connection to a given URL"""

    return Web3(Web3.HTTPProvider(url))


def get_current_block_number(web3):
    """Get the current block number"""

    return web3.eth.blockNumber


def get_eth_filter_logs(web3, token_address, event_topic_signatures, start_block, end_block):
    """Get transfer logs for a given token contract and event topic signature"""

    web3_filter = web3.eth.filter(
            {
                "fromBlock": start_block,
                "toBlock": end_block,
                "address": token_address,
                "topics": [event_topic_signatures],
            }
        )
    return web3.eth.get_filter_logs(web3_filter.filter_id)


def get_transaction_data(web3, tx_hash):
    """Get transaction data for a given transaction hash"""
    
    return web3.eth.get_transaction(tx_hash)


def get_transaction_receipt(web3, tx_hash):
    """Get transaction receipt for a given transaction hash"""
    
    return web3.eth.get_transaction_receipt(tx_hash)


def get_block(web3, block_number):
    """Get the timestamp for a given block number"""
    
    return web3.eth.get_block(block_number)


def process_log(log, web3):
    """Process the logs to get the transfer data"""
    
    this_result = {}
    tx_hash = log['transactionHash']
    tx_data = get_transaction_data(web3, tx_hash)
    print(f'Processing transaction {tx_hash.hex()}...')

    # Process the transaction data
    this_result['gas_limit'] = int(tx_data['gas'])
    this_result['gas_price'] = int(tx_data['gasPrice'])
    this_result['block_number'] = tx_data['blockNumber']
    this_result['from'] = tx_data['from']
    this_result['to'] = tx_data['to']

    # Process the transaction receipt
    tx_receipt = get_transaction_receipt(web3, tx_hash)
    print(f'Processing transaction receipt {tx_receipt}...')
    this_result['gas_used']  = int(tx_receipt['gasUsed'])

    # Get the block timestamp
    block = get_block(web3, this_result['block_number'])
    print(f'Processing block {block}...')
    this_result['timestamp'] = block['timestamp']

    # Process the log data
    this_result['tx_hash'] = tx_hash.hex()
    tx_data = log['data'][2:]
    transfer_data = [tx_data[i : i + 64] for i in range(0, len(tx_data), 64)]
    this_result['transfer_from'] = log.topics[1][-20:].hex()
    this_result['transfer_to'] = log.topics[2][-20:].hex()
    this_result['amount_transfered_hex'] = transfer_data[0]
    this_result['amount_transfered_decimal'] = int(transfer_data[0], 16) / 10e17

    return this_result


def get_target_tx_data(env_vars, start_block=0):
    """Get transfer logs for a given token contract and event topic signature"""

    # Get the environment variables
    rpc_url = env_vars['RPC_PROVIDER_URL']
    chunk = int(env_vars['CHUNK_SIZE'])
    token_address = env_vars['TOKEN_ADDRESS']
    event_topic_signatures = env_vars['TRANSFER_EVENT_TOPIC_HASH']

    # Create a web3 connection
    web3 = create_web3_connection(rpc_url)
    current_block = int(get_current_block_number(web3))
    
    processed_tx = []

    while start_block < current_block:
        
        # Get the transfer logs
        logs = get_eth_filter_logs(web3, token_address, event_topic_signatures, start_block, start_block + chunk)

        if logs is not None:
            for log in logs:
                processed_tx.append(process_log(log, web3))
                sleep(float(env_vars['SLEEP_TIME']))

        start_block += chunk
        
    return processed_tx


if __name__ == '__main__':

    env_data = get_env()
    processed_tx = get_target_tx_data(env_data)
    print(processed_tx)