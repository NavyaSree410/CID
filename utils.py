import random

HIGH_RISK = ["OTP Fraud", "Banking Fraud", "Crypto Scam"]

FOREIGN_KEYWORDS = [
    "gmail.com", "facebook.com", "instagram.com",
    "telegram", "bitcoin", "binance", "cloudflare"
]

def generate_complaint_id():
    return f"CRIME-2026-{random.randint(1000,9999)}"


def detect_priority(fraud_type):
    return "HIGH" if fraud_type in HIGH_RISK else "MEDIUM"


def detect_jurisdiction(description):
    desc = description.lower()

    for k in FOREIGN_KEYWORDS:
        if k in desc:
            return "INTERNATIONAL (MLAT REQUIRED)"

    return "LOCAL CASE"
