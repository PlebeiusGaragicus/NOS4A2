import logging
logger = logging.getLogger("nosferatu")

from typing import Union

import bech32


def npubToHex(npub: str) -> Union[None, str]:
    """ provide a bech32 npub-formatted string, and get back the hex-encoded public key """

    hrpgot, data = bech32.bech32_decode(npub)

    if hrpgot != "npub":
        # TODO
        # logger.critical("Invalid human-readable part (prefix) of the encoded public key.")
        return None

    decoded = bech32.convertbits(data, 5, 8, False)
    if decoded is None:
        # TODO
        # logger.critical("Error decoding the encoded public key.")
        return None

    keyval = ''.join('{:02x}'.format(byte) for byte in decoded)

    return keyval


def nsecToHex(nsec: str) -> Union[None, str]:
    """ provide a bech32 nsec-formatted string, and get back the hex-encoded private key """

    hrpgot, data = bech32.bech32_decode(nsec)

    if hrpgot != "nsec":
        # TODO
        # logger.critical("Invalid human-readable part (prefix) of the encoded private key.")
        return None

    decoded = bech32.convertbits(data, 5, 8, False)
    if decoded is None:
        # TODO
        # logger.critical("Error decoding the encoded private key.")
        return None

    keyval = ''.join('{:02x}'.format(byte) for byte in decoded)

    return keyval


def hexToNpub(hex: str) -> Union[None, str]:
    """ provide a hex-encoded public key, and get back the bech32 npub-formatted string """

    # Decode the hex-encoded public key
    decoded = bytes.fromhex(hex)

    # Convert the public key to bech32
    npub = bech32.bech32_encode("npub", bech32.convertbits(decoded, 8, 5, True))

    return npub



if __name__ == "__main__":
    nsec = input("Enter a nsec-formatted private key: ")
    print(nsecToHex(nsec))








# #  A Bech32_encoded address consists of 3 parts: HRP + Separator + Data: bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4
# # https://en.bitcoin.it/wiki/Bech32
# def nsecToHex(nsec: str) -> Union[None, str]:
#     """ provide a bech32 nsec-formatted string, and get back the hex-encoded private key """

#     # Decode the BASE58 nsec string
#     # keyval = bech32.decode(keyraw)
#     # keyval = bech32.bech32_decode(keyraw)

#     # hrpgot, data = bech32.bech32_decode("nsec", keyraw.split("nsec")[1])
#     hrpgot, data = bech32.bech32_decode(nsec)

#     if hrpgot != "nsec":
#         logger.critical("Invalid human-readable part (prefix) of the encoded private key.")
#         return None
#         # raise ValueError("Invalid human-readable part (prefix) of the encoded private key.")

#     decoded = bech32.convertbits(data, 5, 8, False)
#     if decoded is None:
#         logger.critical("Error decoding the encoded private key.")
#         return None
#         # raise ValueError("Error decoding the encoded private key.")

#     keyval = ''.join('{:02x}'.format(byte) for byte in decoded)

#     return keyval


    # return bech32.decode(nsec).data.toString('hex');
