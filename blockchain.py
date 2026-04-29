import hashlib
import json

chain = []


def add_block(data):
    prev = chain[-1]["hash"] if chain else "0"

    raw = json.dumps(data) + prev
    h = hashlib.sha256(raw.encode()).hexdigest()

    block = {"data": data, "prev": prev, "hash": h}
    chain.append(block)
