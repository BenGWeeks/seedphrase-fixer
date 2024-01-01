import os
import argparse
from dotenv import load_dotenv, find_dotenv
from colorama import Fore, Style

from utils.crypto import BIP39_WORDLIST, is_valid_checksum, calculate_checksum_word, mnemonic_to_seed
from utils.seedphrase_fixer import fix_seedphrase
from utils.check_blockcypher_limits import check_limits
from utils.address_derivation import derive_address_from_seed
from utils.bitcoin_balance_checker import check_bitcoin_balance

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

def calculate_and_check_balance(seedphrase, passphrase):
    # Join the seedphrase list into a string
    seedphrase_str = ' '.join(seedphrase)
    # Calculate the 12th word
    checksum_word = calculate_checksum_word(seedphrase_str)
    possible_seedphrase = seedphrase + [checksum_word]
    # Derive the corresponding Bitcoin address
    seed_bytes = mnemonic_to_seed(' '.join(possible_seedphrase), passphrase)
    address = derive_address_from_seed(seed_bytes)
    # Check the balance of the address
    balance = check_bitcoin_balance(address)
    if balance > 0:
        print(f"Found balance {balance} at address {address} with seedphrase {' '.join(possible_seedphrase)}")

def main():
    parser = argparse.ArgumentParser(description='12th Word Calculator: Calculates the 12th or 24th word of a provided seedphrase and checks Bitcoin balances.')

    parser.add_argument('seedphrase', type=str, nargs='+', help='The first 11 or 23 words of a BIP-39 seedphrase.')
    parser.add_argument('--passphrase', type=str, default='', help='An optional passphrase for additional security.')

    args = parser.parse_args()

    print(f"Seedphrase: {args.seedphrase}")
    print(f"Passphrase: {args.passphrase}")

    calculate_and_check_balance(args.seedphrase, args.passphrase)

if __name__ == '__main__':
    main()
