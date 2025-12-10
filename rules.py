MANDATORY_FIELDS = [
    "policyNumber",
    "policyholderName",
    "incidentDate",
    "claimant",
    "claimType",
    "initialEstimateNumeric",
]


def apply_rules(fields):
    reasons = []
    missing = [f for f in MANDATORY_FIELDS if not fields.get(f)]
    if missing:
        reasons.append(f"Missing mandatory fields: {missing}")
        return "Manual Review", missing, reasons

    desc = (fields.get("description") or "").lower()
    if any(word in desc for word in ["fraud", "staged", "inconsistent"]):
        reasons.append("Description contains suspicious keywords")
        return "Investigation Flag", [], reasons

    claim_type = (fields.get("claimType") or "").lower()
    if "injury" in claim_type:
        reasons.append("Claim type indicates injury")
        return "Specialist Queue", [], reasons

    estimate = fields.get("initialEstimateNumeric")
    if estimate is not None and estimate < 25000:
        reasons.append(f"Estimated damage {estimate} is < 25000")
        return "Fast-track", [], reasons

    reasons.append("Default fallback to Manual Review")
    return "Manual Review", [], reasons
