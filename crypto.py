import random

# The shared encryption key — a 2-digit number (0–99)
# Change this number to re-key all future uploads.
ENCRYPTION_KEY = 42


def _keystream(key: int, length: int) -> bytes:
    """Generate a deterministic pseudo-random byte stream seeded by key."""
    rng = random.Random(key)
    return bytes(rng.randint(0, 255) for _ in range(length))


def encrypt_bytes(data: bytes, key: int) -> bytes:
    """XOR data with a keystream derived from key."""
    stream = _keystream(key, len(data))
    return bytes(b ^ k for b, k in zip(data, stream))


# Decryption is identical to encryption (XOR is its own inverse)
decrypt_bytes = encrypt_bytes
