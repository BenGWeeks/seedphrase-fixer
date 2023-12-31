from utils.crypto import is_valid_checksum, BIP39_WORDLIST
from utils.bitcoin_address_validation import validate_with_bitcoin_address


def fix_seedphrase(seedphrase, passphrase, replace_index=None):
    words = seedphrase.split()
    valid_checksum_indices = []
    balances = {'P2PKH': 0, 'P2SH': 0, 'Bech32': 0}  # New balances dictionary with all address types

    indices_to_try = range(len(words) - 1) if replace_index is None else [replace_index]
    for i in indices_to_try:  # Exclude the last word which serves as a checksum
        original_word = words[i]
        for candidate in BIP39_WORDLIST:
            words[i] = candidate
            candidate_seedphrase = ' '.join(words)
            if is_valid_checksum(candidate_seedphrase, BIP39_WORDLIST):
                if validate_with_bitcoin_address(candidate_seedphrase, passphrase):
                    print(f'Valid checksum with word "{candidate}" at position {i}')
                    print(f"Candidate Seedphrase: {candidate_seedphrase}")
                    print("Balances:")
                    for address_type in ['P2PKH', 'P2SH', 'Bech32']:
                        balance = balances.get(address_type, 0)
                        print(f"{address_type}: {balance}")
                    if any(value > 0 for value in balances.values()):
                        return candidate_seedphrase, balances  # Return balances along with seedphrase
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
