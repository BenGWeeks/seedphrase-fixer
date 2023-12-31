import requests
import logging

logging.basicConfig(filename='seedphrase_fixer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_bitcoin_balance(address):
    bitcoin_api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    try:
        response = requests.get(bitcoin_api_url)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Checking balance for address: {address}. Balance found: {data['final_balance']}")
        return data['final_balance']
    except (requests.exceptions.HTTPError, Exception) as err:
        logging.error(f"An error occurred: {err}")
        return 0
