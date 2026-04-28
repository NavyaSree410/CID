def detect_jurisdiction(text):
    signals = ["gmail", "facebook", "paypal", "bitcoin", "binance", "server", "cloud"]

    for s in signals:
        if s in text.lower():
            return "INTERNATIONAL (MLAT REQUIRED)"

    return "LOCAL (INDIA)"
