import hashlib
from mnemonic import Mnemonic

def is_valid_checksum(seedphrase, wordlist):
    """
    Validates the checksum of the given seedphrase.

    :param seedphrase: The BIP-39 mnemonic seedphrase string.
    :param wordlist: List of words according to BIP-39 English wordlist.
    :return: Boolean indicating whether the checksum is valid.
    """
    words = seedphrase.split()
    indices = [wordlist.index(word) for word in words]
    bits = ''.join(bin(index)[2:].zfill(11) for index in indices)
    checksum_length = len(words) // 3
    entropy_bits = bits[:-checksum_length]
    checksum_bits = bits[-checksum_length:]
    hash_digest = hashlib.sha256(int(entropy_bits, 2).to_bytes((len(entropy_bits) + 7) // 8, byteorder='big')).digest()
    hash_bits = bin(int.from_bytes(hash_digest, byteorder='big'))[2:].zfill(256)[:checksum_length]
    return hash_bits == checksum_bits

mnemo = Mnemonic("english")
BIP39_WORDLIST = mnemo.wordlist
def calculate_checksum_word(seedphrase):
    """
    Calculates the 12th word of the given seedphrase.

    :param seedphrase: The first 11 words of a BIP-39 seedphrase.
    :return: The 12th word of the seedphrase.
    """
    words = seedphrase.split()
    indices = [BIP39_WORDLIST.index(word) for word in words]
    bits = ''.join(bin(index)[2:].zfill(11) for index in indices)
    checksum_length = len(bits) // 33
    entropy_bits = bits[:len(bits)-checksum_length]
    checksum_bits = bits[len(bits)-checksum_length:]
    entropy = int(entropy_bits, 2)
    checksum = int(checksum_bits, 2)
    entropy_bytes = entropy.to_bytes((entropy.bit_length() + 7) // 8, 'big')
    hashed_entropy = hashlib.sha256(entropy_bytes).digest()
    hashed_entropy_bits = bin(int.from_bytes(hashed_entropy, 'big'))[2:].zfill(256)
    checksum_calculated = int(hashed_entropy_bits[:checksum_length], 2)
    if checksum == checksum_calculated:
        return words[-1]
    else:
        for i in range(2**checksum_length):
            test_checksum = bin(i)[2:].zfill(checksum_length)
            if int(test_checksum, 2) == checksum_calculated:
                return BIP39_WORDLIST[i]
    return None

def mnemonic_to_seed(mnemonic, passphrase=''):
    """
    Converts a mnemonic seedphrase into a seed.

    :param mnemonic: The BIP-39 mnemonic seedphrase string.
    :param passphrase: An optional passphrase for additional security.
    :return: The seed corresponding to the mnemonic.
    """
    mnemo = Mnemonic("english")
    return mnemo.to_seed(mnemonic, passphrase)
