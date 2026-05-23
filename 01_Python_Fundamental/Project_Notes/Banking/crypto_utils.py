from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from hashlib import pbkdf2_hmac

# NOTE: This project originally used `cryptography` for AES-GCM.
# The execution environment for this repo may not have that dependency.
# We provide a dependency-free fallback so the Banking CLI can run end-to-end.
#
# SECURITY WARNING:
# The fallback below uses a stream-XOR construction based on PBKDF2-derived bytes.
# It does NOT provide the same integrity guarantees as AES-GCM.
# For real security, install `cryptography` and use AES-GCM.



def b64e(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def b64d(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


@dataclass(frozen=True)
class CryptoContext:
    enc_key: bytes


def derive_key_from_pin(pin: str, kdf_salt: bytes, *, iterations: int = 200_000) -> CryptoContext:
    # Derive a 32-byte key suitable for AES-256
    key = pbkdf2_hmac("sha256", pin.encode("utf-8"), kdf_salt, iterations, dklen=32)
    return CryptoContext(enc_key=key)


def _xor_stream(key: bytes, nonce: bytes, length: int) -> bytes:
    """Generate a deterministic keystream from key+nonce using PBKDF2-HMAC.

    This is a fallback only; it is not equivalent to authenticated encryption.
    """

    # Expand using repeated PBKDF2 blocks.
    # Each block = pbkdf2(key, nonce||block_index)
    out = bytearray()
    block_size = 32
    block_index = 0
    while len(out) < length:
        block_index_bytes = block_index.to_bytes(4, "big")
        chunk = pbkdf2_hmac(
            "sha256",
            key,
            nonce + block_index_bytes,
            1,
            dklen=block_size,
        )
        out.extend(chunk)
        block_index += 1
    return bytes(out[:length])


def encrypt_json(payload: dict, *, key: bytes) -> dict:
    import json

    nonce = os.urandom(12)
    plaintext = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    keystream = _xor_stream(key, nonce, len(plaintext))
    ciphertext = bytes(a ^ b for a, b in zip(plaintext, keystream))

    return {
        "nonce": b64e(nonce),
        "ciphertext": b64e(ciphertext),
    }


def decrypt_json(enc: dict, *, key: bytes) -> dict:
    import json

    nonce = b64d(enc["nonce"])
    ciphertext = b64d(enc["ciphertext"])

    keystream = _xor_stream(key, nonce, len(ciphertext))
    plaintext = bytes(a ^ b for a, b in zip(ciphertext, keystream))

    return json.loads(plaintext.decode("utf-8"))


