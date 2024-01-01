import logging
from ecdsa import SigningKey, SECP256k1
from bip_utils import Bip39SeedGenerator, Bip44, Bip49, Bip84, Bip44Coins, Bip84Coins, Bip44Changes, Bip49Coins

def derive_address_from_seed(seed_bytes):
    addresses = {}
    # P2PKH
    bip32_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip32_ctx = bip32_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    addresses['P2PKH'] = bip32_ctx.PublicKey().ToAddress()
    # P2SH
    bip32_ctx = Bip49.FromSeed(seed_bytes, Bip49Coins.BITCOIN)
    bip32_ctx = bip32_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    addresses['P2SH'] = bip32_ctx.PublicKey().ToAddress()
    # Bech32
    bip84_ctx = Bip84.FromSeed(seed_bytes, Bip84Coins.BITCOIN)
    bip84_ctx = bip84_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    addresses['Bech32'] = bip84_ctx.PublicKey().ToAddress()

    return addresses

def derive_multiple_address_types(mnemonic, passphrase=""):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate(passphrase)
    addresses = {
        'P2PKH': derive_address_from_seed(seed_bytes),
        'P2SH': derive_address_from_seed(seed_bytes),
        'bech32': derive_address_from_seed(seed_bytes),
    }
    logging.info(f"Deriving addresses for seedphrase: {mnemonic}. Addresses derived: {addresses}")
    return addresses
