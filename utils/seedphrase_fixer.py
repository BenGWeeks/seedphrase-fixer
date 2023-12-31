from bip_utils.utils.mnemonic.mnemonic_ex import MnemonicChecksumError
from colorama import Fore, Style
from utils.crypto import is_valid_checksum, BIP39_WORDLIST
from utils.bitcoin_address_validation import validate_with_bitcoin_address
from utils.bitcoin_balance_checker import check_bitcoin_balance
from utils.address_derivation import derive_multiple_address_types


def fix_seedphrase(seedphrase, passphrase, replace_index=None):
    words = seedphrase.split()
    valid_checksum_indices = []
    balances = {'P2PKH': 0, 'P2SH': 0, 'Bech32': 0}  # New balances dictionary with all address types

    # Check if the original seedphrase has a balance
    try:
        addresses = derive_multiple_address_types(seedphrase, passphrase)
    except MnemonicChecksumError:
        print(f"{Fore.RED}Invalid checksum for seedphrase: {seedphrase}{Style.RESET_ALL}")
        print("helloworld2")
        addresses = None
    #print(f"Addresses: {addresses}")
    if addresses is None:
        return None, balances
    balances = {address_type: check_bitcoin_balance(address) for address_type, address in addresses.items()}
    #print(f"Balances: {balances}")
    if any(value > 0 for value in balances.values()):
        print("helloworld3")
        return seedphrase, balances  # Return balances along with seedphrase

    if replace_index is not None:
        original_word = words[replace_index]
        for candidate in BIP39_WORDLIST:
            words[replace_index] = candidate
            candidate_seedphrase = ' '.join(words)
            print("helloworld4")
            if is_valid_checksum(candidate_seedphrase, BIP39_WORDLIST):
                print(f'Valid checksum with word "{candidate}" at position {replace_index}')
                print(f"Candidate Seedphrase: {candidate_seedphrase}")
                addresses = derive_multiple_address_types(candidate_seedphrase, passphrase)
                print("helloworld5")
                if addresses is None:
                    continue
                balances = {address_type: check_bitcoin_balance(address) for address_type, address in addresses.items()}
                print("Balances:")
                for address_type in ['P2PKH', 'P2SH', 'Bech32']:
                    balance = balances.get(address_type, 0)
                    print(f"{address_type}: {balance}")
                    print("helloworld6")
                if any(value > 0 for value in balances.values()):
                    print("helloworld7")
                    return candidate_seedphrase, balances  # Return balances along with seedphrase
            # else:
                # break
        print("helloworld8")
        words[replace_index] = original_word
    else:
        print("helloworld9")
        indices_to_try = range(len(words) - 1)  # Exclude the last word which serves as a checksum
        for i in indices_to_try:
            original_word = words[i]
            for candidate in BIP39_WORDLIST:
                words[i] = candidate
                candidate_seedphrase = ' '.join(words)
                print("helloworld10")
                if is_valid_checksum(candidate_seedphrase, BIP39_WORDLIST):
                    if validate_with_bitcoin_address(candidate_seedphrase, passphrase):
                        print(f'Valid checksum with word "{candidate}" at position {i}')
                        print(f"Candidate Seedphrase: {candidate_seedphrase}")
                        addresses = derive_multiple_address_types(candidate_seedphrase, passphrase)
                        balances = {address_type: check_bitcoin_balance(address) for address_type, address in addresses.items()}
                        print("Balances:")
                        for address_type in ['P2PKH', 'P2SH', 'Bech32']:
                            balance = balances.get(address_type, 0)
                            print(f"{address_type}: {balance}")
                        if any(value > 0 for value in balances.values()):
                            return candidate_seedphrase, balances  # Return balances along with seedphrase
                        else:
                            valid_checksum_indices.append(i)
            words[i] = original_word

    # If replace_index is None, we need to try the remaining valid checksum indices
    if replace_index is None and len(valid_checksum_indices) > 0:
        for index in valid_checksum_indices:
            for candidate in BIP39_WORDLIST:
                words[index] = candidate
                candidate_seedphrase = ' '.join(words)
                if validate_with_bitcoin_address(candidate_seedphrase, passphrase):
                    return candidate_seedphrase, balances  # Return balances along with seedphrase
            words[index] = original_word
    
    return None, balances  # Return balances even if no corrected seedphrase is found
