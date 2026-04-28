import random

HIGH_RISK = ["OTP Fraud", "Banking Fraud", "Crypto Scam"]

FOREIGN_SIGNS = [
    "gmail.com", "facebook.com", "instagram.com",
    "telegram", "binance", "bitcoin", "paypal",
    "cloudflare", "amazon", "apple id"
]


def generate_complaint_id():
    return f"CRIME-2026-{random.randint(1000,9999)}"


def detect_priority(fraud_type):
    return "HIGH" if fraud_type in HIGH_RISK else "MEDIUM"


def detect_jurisdiction(text):
    text = text.lower()

    for i in FOREIGN_SIGNS:
        if i in text:
            return "INTERNATIONAL (MLAT REQUIRED)"

    return "LOCAL CASE"
