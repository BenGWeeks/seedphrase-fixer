from ecdsa import SigningKey, SECP256k1
from bip_utils import Bip39SeedGenerator, Bip44, Bip49, Bip84


def derive_address_from_seed(seed_bytes, address_type='P2PKH'):
    bip32_ctx = Bip44.FromSeed(seed_bytes)
    
    if address_type == 'P2PKH':
        address = bip32_ctx.P2pkhAddress().ToString()
    elif address_type == 'P2SH':
        bip32_ctx = Bip49.FromSeed(seed_bytes)
        address = bip32_ctx.P2shP2wpkhAddress().ToString()
    elif address_type == 'bech32':
        bip32_ctx = Bip84.FromSeed(seed_bytes)
        address = bip32_ctx.P2wpkhAddress().ToString()
    else:
        raise ValueError("Unsupported address type")
        
    return address


def derive_multiple_address_types(mnemonic, passphrase=""):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    return {
        'P2PKH': derive_address_from_seed(seed_bytes, 'P2PKH'),
        'P2SH': derive_address_from_seed(seed_bytes, 'P2SH'),
        'bech32': derive_address_from_seed(seed_bytes, 'bech32'),
    }
