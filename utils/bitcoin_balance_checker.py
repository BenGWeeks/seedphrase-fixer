import requests
import logging

logging.basicConfig(filename='seedphrase_fixer.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_bitcoin_balance(address):
    bitcoin_api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    try:
        response = requests.get(bitcoin_api_url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        data = response.json()
        return data['final_balance']
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")  # INPUT_REQUIRED {The Bitcoin API endpoint URL might change; ensure it's the correct endpoint for retrieving balances}  
    except Exception as err:
        logging.error(f"An error occurred: {err}")
    return None
