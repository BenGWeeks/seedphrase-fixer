import os
import argparse

from utils.bitcoin_balance_checker import check_bitcoin_balance
try:
    from dotenv import load_dotenv, find_dotenv
except ModuleNotFoundError:
    print("Module 'dotenv' not found. Please install it using 'pip install python-dotenv'")
    exit(1)
from colorama import Fore, Style

from utils.crypto import BIP39_WORDLIST, is_valid_checksum
from utils.seedphrase_fixer import fix_seedphrase
from utils.check_blockcypher_limits import check_limits

# Load environment variables from .env file
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path, override=True)
else:
    print("Could not find .env file. Please ensure it exists.")
    exit(1)

# Get BlockCypher API token
BLOCKCYPHER_TOKEN = os.getenv('BLOCKCYPHER_TOKEN')
if not BLOCKCYPHER_TOKEN:
    print("Environment variable 'BLOCKCYPHER_TOKEN' not found in .env file. Please add it.")
    exit(1)

# Check BlockCypher API usage
if check_limits():
    print(f"{Fore.GREEN}BlockCypher API usage is OK{Style.RESET_ALL}")
else:
    print(f"{Fore.RED}BlockCypher API usage is over the limit{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='Seedphrase Fixer: Corrects a single wrong word in a provided seedphrase and checks Bitcoin balances.')

    parser.add_argument('seedphrase', type=str, help='A 12 or 24 word BIP-39 seedphrase.')
    parser.add_argument('passphrase', type=str, nargs='?', default='', help='An optional passphrase for additional security.')
    parser.add_argument('replace_index', type=int, nargs='?', default=None, help='The index of the word to replace. If not provided, all words will be tried.')

    args = parser.parse_args()

    print(f"Seedphrase: {args.seedphrase}")
    print(f"Passphrase: {args.passphrase}")
    from utils.address_derivation import derive_multiple_address_types

    print(f"Replace Index: {args.replace_index}")




    # Let's first check the seedphrase we are given to see if it contains any balances.
    if not is_valid_checksum(args.seedphrase, BIP39_WORDLIST):
        print("The supplied seedphrase is not a valid checksum, let's try and fix it.")
    else:
        print("The supplied seedphrase is at least a valid checksum, let's see if it has any balances.")
        addresses = derive_multiple_address_types(args.seedphrase, args.passphrase)
        balances = {address_type: check_bitcoin_balance(address) for address_type, address in addresses.items()}
        if any(value > 0 for value in balances.values()):
            print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}")
            print("The seedphrase has a balance and (presumably) doesn't need fixing.")
        return
    
    corrected_seedphrase, balances = fix_seedphrase(args.seedphrase, args.passphrase, args.replace_index)

    if corrected_seedphrase:
        print(f"{Fore.GREEN}SUCCESS{Style.RESET_ALL}")
        print(f"Corrected Seedphrase: {corrected_seedphrase}")
        print(f"Seedphrase: {args.seedphrase}")
        if args.passphrase:
            print(f"Passphrase: {args.passphrase}")
        for address_type, balance in balances.items():
            if balance > 0:
                print(f"{Fore.GREEN}{address_type}: {balance}{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTYELLOW_EX}{address_type}: {balance}{Style.RESET_ALL}")
    else:
        print("Could not find a balance using all the BIP-39 words at that positions. It may have another word that is incorrect, have more than one error, or never had any funds on it.")

if __name__ == '__main__':
    main()
