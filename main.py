import argparse

from utils.crypto import BIP39_WORDLIST
from utils.seedphrase_fixer import fix_seedphrase

def main():
    parser = argparse.ArgumentParser(description='Seedphrase Fixer: Corrects a single wrong word in a provided seedphrase and checks Bitcoin balances.')

    parser.add_argument('seedphrase', type=str, help='A 12 or 24 word BIP-39 seedphrase.')
    parser.add_argument('passphrase', type=str, nargs='?', default='', help='An optional passphrase for additional security.')

    args = parser.parse_args()

    #corrected_seedphrase = fix_seedphrase(args.seedphrase)
    corrected_seedphrase, balances = fix_seedphrase(args.seedphrase, args.passphrase)
    if corrected_seedphrase:
        print(f"Corrected Seedphrase: {corrected_seedphrase}")
        print(f"Seedphrase: {args.seedphrase}")
        if args.passphrase:
            print(f"Passphrase: {args.passphrase}")
        print("Balances:")
        for address_type in ['P2PKH', 'P2SH', 'Bech32']:
            print(f"{address_type}: {balances.get(address_type, 0)}")
    else:
        print("Could not find an incorrect word to replace. The seedphrase might already be correct or have more than one incorrect word.")

if __name__ == '__main__':
    main()
