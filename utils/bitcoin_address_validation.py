from utils.address_derivation import derive_multiple_address_types
from utils.bitcoin_balance_checker import check_bitcoin_balance
import requests

def validate_with_bitcoin_address(mnemonic, passphrase):
    addresses = derive_multiple_address_types(mnemonic, passphrase)
    
    balances = {}
    for address_type, btc_address in addresses.items():
        balance = check_bitcoin_balance(btc_address)
        if balance is not None:  # If the balance check was successful
            balances[address_type] = balance

    if balances:
        return balances
    return None
