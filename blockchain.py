import hashlib
import json
from datetime import datetime

chain = []


def add_block(data):
    prev = chain[-1]["hash"] if chain else "0"

    raw = json.dumps(data) + prev + str(datetime.now())
    h = hashlib.sha256(raw.encode()).hexdigest()

    block = {
        "data": data,
        "prev_hash": prev,
        "hash": h,
        "time": str(datetime.now())
    }

    chain.append(block)
    return block
