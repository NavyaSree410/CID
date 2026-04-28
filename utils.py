import time

def generate_case_id():
    return "CASE-" + str(int(time.time() * 1000))
