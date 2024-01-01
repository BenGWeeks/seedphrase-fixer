import os
import time
import requests
import logging
from colorama import Fore, Style

logging.basicConfig(filename='seedphrase_fixer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_bitcoin_balance(addresses):
    for address_type, address in addresses.items():
        token = os.getenv('BLOCKCYPHER_TOKEN')
        bitcoin_api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address['P2PKH']}/balance?token={token}"
        bitcoin_api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address['P2SH']}/balance?token={token}"
        bitcoin_api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address['Bech32']}/balance?token={token}"
    try:
        time.sleep(1)  # Add a delay before each API request
        response = requests.get(bitcoin_api_url)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Checking balance for address: {address}. Balance found: {data['final_balance']}")
        if data['final_balance'] == 0:
            print(f"{Fore.LIGHTYELLOW_EX}Checking balance for address: {address}. Balance found: {data['final_balance']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}Checking balance for address: {address}. Balance found: {data['final_balance']}{Style.RESET_ALL}")
        return data['final_balance']
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 429:
            print("Too many requests. Please wait and try again later.")
            logging.error("Too many requests. Please wait and try again later.")
        else:
            print(f"HTTP error occurred: {http_err}")
            logging.error(f"HTTP error occurred: {http_err}")
        return 0
    except Exception as err:
        print(f"Other error occurred: {err}")
        logging.error(f"Other error occurred: {err}")
        return 0
