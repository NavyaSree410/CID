def detect_jurisdiction(text):
    keywords = ["gmail", "facebook", "paypal", "bitcoin", "server", "binance"]

    text = text.lower()

    for k in keywords:
        if k in text:
            return "INTERNATIONAL (MLAT REQUIRED)"

    return "LOCAL (INDIA)"
