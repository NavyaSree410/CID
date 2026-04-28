import hashlib
import json
from datetime import datetime

chain = []


def create_hash(data, prev_hash):
    block = str(data) + str(prev_hash) + str(datetime.now())
    return hashlib.sha256(block.encode()).hexdigest()


def add_block(data):
    prev_hash = chain[-1]["hash"] if chain else "0"

    block = {
        "data": data,
        "timestamp": str(datetime.now()),
        "prev_hash": prev_hash,
        "hash": ""
    }

    block["hash"] = create_hash(data, prev_hash)

    chain.append(block)
    return block
