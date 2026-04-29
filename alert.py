alerts = []


def trigger_alert(case_id, location, unit):
    alerts.append({
        "case_id": case_id,
        "location": location,
        "unit": unit,
        "status": "ACTIVE"
    })
