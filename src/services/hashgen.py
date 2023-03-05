import argon2
import secrets
import hashlib

ph = argon2.PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=2,
    hash_len=32,
    salt_len=16,
    encoding="utf-8",
)


class HashGenerator:
    def __init__(self):
        self._hash = None

    def gen(self, data: str):
        hashed_data = ph.hash(data)
        return hashed_data

    def verify(self, hash: str, data: str):
        return ph.verify(hash, data)
