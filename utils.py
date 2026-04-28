import random

HIGH_RISK = ["OTP Fraud", "Banking Fraud", "Crypto Scam"]

def generate_id():
    return f"CRIME-2026-{random.randint(1000,9999)}"


def priority(fraud):
    return "HIGH" if fraud in HIGH_RISK else "MEDIUM"


# SIMPLE SIMILARITY LINKING ENGINE
def similarity_score(a, b):
    a, b = a.lower(), b.lower()
    return len(set(a.split()) & set(b.split()))


def find_similar(existing_cases, new_desc):
    linked = []

    for case in existing_cases:
        score = similarity_score(case["description"], new_desc)
        if score >= 2:
            linked.append(case["complaint_id"])

    return linked
