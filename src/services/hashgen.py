import hashlib


class HashGenerator:
    def __init__(self):
        self._hash = None

    def gen(self, data: str):
        hashed_data = hashlib.sha3_512(data).hexdigest()
        return hashed_data
