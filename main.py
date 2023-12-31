import os
import argparse
try:
    from dotenv import load_dotenv, find_dotenv
except ModuleNotFoundError:
    print("Module 'dotenv' not found. Please install it using 'pip install python-dotenv'")
    exit(1)
from colorama import Fore, Style

from utils.crypto import BIP39_WORDLIST
from utils.seedphrase_fixer import fix_seedphrase
from utils.check_blockcypher_limits import check_limits

# Load environment variables from .env file
load_dotenv(find_dotenv(), override=True)

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
    print(f"Replace Index: {args.replace_index}")

    corrected_seedphrase, balances = fix_seedphrase(args.seedphrase, args.passphrase, args.replace_index)

    print(f"Corrected Seedphrase: {corrected_seedphrase}")
    print(f"Balances: {balances}")
    if corrected_seedphrase:
        print(f"Corrected Seedphrase: {corrected_seedphrase}")
        print(f"Seedphrase: {args.seedphrase}")
        if args.passphrase:
            print(f"Passphrase: {args.passphrase}")
        print("Balances:")
        for address_type in ['P2PKH', 'P2SH', 'Bech32']:
            balance = balances.get(address_type, 0)
            if balance == 0:
                print(f"{Fore.LIGHTYELLOW_EX}{address_type}: {balance}{Style.RESET_ALL}")
            else:
                print(f"{address_type}: {balance}")
    else:
        print("Could not find an incorrect word to replace. The seedphrase might already be correct or have more than one incorrect word.")

if __name__ == '__main__':
    main()
