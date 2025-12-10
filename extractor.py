import re
from dateutil import parser


def normalize(value):
    if not value:
        return
    s = str(value)
    s = s.replace(",", "")
    m = re.search(r"(\d+)", s)
    if m:
        try:
            return int(m.group(1))
        except:
            return None
    return None


def extract_field(pattern, text):
    if not text:
        return None
    m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def extract_fields(text):
    fields = {
        "policyNumber": extract_field(r"Policy Number[:\s]*([\w\-]+)", text),
        "policyholderName": extract_field(
            r"Policyholder Name[:\s]*([A-Za-z0-9 .]+)", text
        ),
        "effectiveDate": extract_field(
            r"Effective Date[:\s]*([0-9\/\-\sA-Za-z]+)", text
        ),
        "incidentDate": extract_field(r"Incident Date[:\s]*([0-9\/\-\sA-Za-z]+)", text),
        "time": extract_field(r"Time[:\s]*([0-9:\sAPMapm\.]+)", text),
        "location": extract_field(r"Location[:\s]*([^\n]+)", text),
        "description": extract_field(
            r"Description[:\s]*([\s\S]*?)(?:\n[A-Z][a-zA-Z ]*:|$)", text
        ),
        "claimant": extract_field(r"Claimant[:\s]*([A-Za-z0-9 .]+)", text),
        "thirdParties": extract_field(r"Third Parties[:\s]*([^\n]+)", text),
        "contact": extract_field(r"Contact[:\s]*([^\n]+)", text),
        "assetType": extract_field(r"Asset Type[:\s]*([A-Za-z0-9 ]+)", text),
        "assetID": extract_field(r"Asset ID[:\s]*([A-Za-z0-9\-]+)", text),
        "estimatedDamage": extract_field(r"Estimated Damage[:\s]*([^\n]+)", text),
        "claimType": extract_field(r"Claim Type[:\s]*([A-Za-z ]+)", text),
        "attachments": extract_field(r"Attachments[:\s]*([^\n]+)", text),
        "initialEstimate": extract_field(r"Initial Estimate[:\s]*([0-9,]+)", text),
    }

    fields["initialEstimateNumeric"] = normalize(
        fields.get("initialEstimate") or fields.get("estimatedDamage")
    )

    for d in ("effectiveDate", "incidentDate"):
        raw = fields.get(d)
        if raw:
            try:
                dt = parser.parse(raw, dayfirst=False, fuzzy=True)
                fields[d] = dt.date().isoformat()
            except:
                fields[d] = raw

    return fields
