import logging
from ecdsa import SigningKey, SECP256k1
from bip_utils import Bip39SeedGenerator, Bip44, Bip49, Bip84, Bip44Coins, Bip84Coins, Bip44Changes, Bip49Coins

def derive_address_from_seed(seed_bytes, address_type='P2PKH'):
    if address_type == 'P2PKH':
        bip32_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
        # External chain is used for main addresses
        bip32_ctx = bip32_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip32_ctx.PublicKey().ToAddress()
    elif address_type == 'P2SH':
        bip32_ctx = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)
        bip32_ctx = bip32_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip32_ctx.PublicKey().ToAddress()
    elif address_type == 'bech32':
        bip32_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
        bip32_ctx = bip32_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
        address = bip32_ctx.PublicKey().ToP2wpkhAddress()
    else:
        print(f"\033[91mUnsupported address type: {address_type}\033[0m")
        address = None

    return address

def derive_multiple_address_types(mnemonic, passphrase=""):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    addresses = {
        'P2PKH': derive_address_from_seed(seed_bytes, 'P2PKH'),
        'P2SH': derive_address_from_seed(seed_bytes, 'P2SH'),
        'bech32': derive_address_from_seed(seed_bytes, 'bech32'),
    }
    logging.info(f"Deriving addresses for seedphrase: {mnemonic}. Addresses derived: {addresses}")
    return addresses
