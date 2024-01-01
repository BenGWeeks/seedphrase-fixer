import os
import argparse
from dotenv import load_dotenv, find_dotenv
from colorama import Fore, Style

from utils.crypto import BIP39_WORDLIST
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

def calculate_and_check_balance(seedphrase, passphrase):
    # TODO: Implement the function to calculate the 12th or 24th word and check the balance

def main():
    parser = argparse.ArgumentParser(description='12th Word Calculator: Calculates the 12th or 24th word of a provided seedphrase and checks Bitcoin balances.')

    parser.add_argument('seedphrase', type=str, help='The first 11 or 23 words of a BIP-39 seedphrase.')
    parser.add_argument('passphrase', type=str, nargs='?', default='', help='An optional passphrase for additional security.')

    args = parser.parse_args()

    print(f"Seedphrase: {args.seedphrase}")
    print(f"Passphrase: {args.passphrase}")

    calculate_and_check_balance(args.seedphrase, args.passphrase)

if __name__ == '__main__':
    main()
