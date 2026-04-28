alerts = []


def trigger_alert(case_id, location, police_unit):
    alert = {
        "case_id": case_id,
        "location": location,
        "police_unit": police_unit,
        "status": "ACTIVE MLAT ALERT"
    }

    alerts.append(alert)
    return alert
