from utils.crypto import is_valid_checksum, BIP39_WORDLIST
from utils.bitcoin_address_validation import validate_with_bitcoin_address


def fix_seedphrase(seedphrase, passphrase):
    words = seedphrase.split()
    valid_checksum_indices = []
    balances = {}  # New balances dictionary

    for i in range(len(words) - 1):  # Exclude the last word which serves as a checksum
        original_word = words[i]
        for candidate in BIP39_WORDLIST:
            words[i] = candidate
            candidate_seedphrase = ' '.join(words)
            if is_valid_checksum(candidate_seedphrase, BIP39_WORDLIST):
                print(f'Valid checksum with word "{candidate}" at position {i}')
                if validate_with_bitcoin_address(candidate_seedphrase, passphrase):
                    return candidate_seedphrase, balances  # Return balances along with seedphrase
                else:
                    valid_checksum_indices.append(i)
                break
        words[i] = original_word

    if len(valid_checksum_indices) > 0:
        for index in valid_checksum_indices:
            for candidate in BIP39_WORDLIST:
                words[index] = candidate
                candidate_seedphrase = ' '.join(words)
                if validate_with_bitcoin_address(candidate_seedphrase, passphrase):
                    return candidate_seedphrase, balances  # Return balances along with seedphrase
            words[index] = original_word
    
    return None, balances  # Return balances even if no corrected seedphrase is found
