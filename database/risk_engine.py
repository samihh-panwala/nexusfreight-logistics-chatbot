from datetime import datetime


# ==========================================
# Calculate Delay Days
# ==========================================

def calculate_delay_days(shipment):

    today = datetime.today().date()

    expected = shipment.get("expected_delivery_date")

    actual = shipment.get("actual_delivery_date")

    try:

        if actual:
            end_date = datetime.strptime(actual, "%Y-%m-%d").date()
        else:
            end_date = today

        expected_date = datetime.strptime(expected, "%Y-%m-%d").date()

        delay = (end_date - expected_date).days

        if delay < 0:
            delay = 0

        return delay

    except Exception:

        return 0


# ==========================================
# Recommended Action
# ==========================================

def recommended_action(level):

    if level == "HIGH":
        return "Escalate immediately to the logistics operations team."

    if level == "MEDIUM":
        return "Monitor shipment closely and coordinate with carrier."

    return "Continue regular shipment tracking."


# ==========================================
# Risk Score
# ==========================================

def risk_score(delay_days, delay_reason=""):

    reason = delay_reason.lower()

    # HIGH RISK
    if delay_days > 5 or "custom" in reason:

        return {
            "risk_level": "HIGH",
            "risk_description": "Shipment requires immediate attention.",
            "classification_reason":
                "Delay is greater than 5 days or customs issue detected."
        }

    # MEDIUM RISK
    if 2 <= delay_days <= 5:

        return {
            "risk_level": "MEDIUM",
            "risk_description": "Shipment is moderately delayed.",
            "classification_reason":
                "Delay is between 2 and 5 days."
        }

    # LOW RISK
    return {
        "risk_level": "LOW",
        "risk_description": "Shipment is operating normally.",
        "classification_reason":
            "Delay is between 0 and 1 day."
    }


# ==========================================
# Shipment Risk
# ==========================================

def shipment_risk(shipment):

    delay_days = calculate_delay_days(shipment)

    delay_reason = shipment.get("delay_reason", "")

    risk = risk_score(
        delay_days,
        delay_reason
    )

    shipment["delay_days"] = delay_days

    shipment["risk_level"] = risk["risk_level"]

    shipment["risk_description"] = risk["risk_description"]

    shipment["classification_reason"] = risk["classification_reason"]

    shipment["recommended_action"] = recommended_action(
        risk["risk_level"]
    )

    return shipment


def build_risk_report(shipments):

    high = 0
    medium = 0
    low = 0

    high_shipments = []
    medium_shipments = []
    low_shipments = []

    for shipment in shipments:

        shipment = shipment_risk(shipment)

        if shipment["risk_level"] == "HIGH":

            high += 1
            high_shipments.append(shipment)

        elif shipment["risk_level"] == "MEDIUM":

            medium += 1
            medium_shipments.append(shipment)

        else:

            low += 1
            low_shipments.append(shipment)

    return {

        "summary": {

            "high_risk": high,
            "medium_risk": medium,
            "low_risk": low

        },

        "high_risk_shipments": high_shipments,

        "medium_risk_shipments": medium_shipments,

        "low_risk_shipments": low_shipments,

        "all_shipments":
            high_shipments +
            medium_shipments +
            low_shipments
    }