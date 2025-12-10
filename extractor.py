mport re
from dateutil import parser



def normalize(value):
    if not value:
        return None
    s = str(value).replace(",", "")
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

    fields = {}

    fields.update({
        "policyNumber": extract_field(r"Policy Number[:\s]*([\w\-]+)", text),
        "policyholderName": extract_field(r"Policyholder Name[:\s]*([A-Za-z0-9 .]+)", text),
        "effectiveDate": extract_field(r"Effective Date[:\s]*([0-9\/\-\sA-Za-z]+)", text),
        "incidentDate": extract_field(r"Incident Date[:\s]*([0-9\/\-\sA-Za-z]+)", text),
        "time": extract_field(r"Time[:\s]*([0-9:\sAPMapm\.]+)", text),
        "location": extract_field(r"Location[:\s]*([^\n]+)", text),
        "description": extract_field(r"Description[:\s]*([\s\S]*?)(?:\n[A-Z][a-zA-Z ]*:|$)", text),
        "claimant": extract_field(r"Claimant[:\s]*([A-Za-z0-9 .]+)", text),
        "thirdParties": extract_field(r"Third Parties[:\s]*([^\n]+)", text),
        "contact": extract_field(r"Contact[:\s]*([^\n]+)", text),
        "assetType": extract_field(r"Asset Type[:\s]*([A-Za-z0-9 ]+)", text),
        "assetID": extract_field(r"Asset ID[:\s]*([A-Za-z0-9\-]+)", text),
        "estimatedDamage": extract_field(r"Estimated Damage[:\s]*([^\n]+)", text),
        "claimType": extract_field(r"Claim Type[:\s]*([A-Za-z ]+)", text),
        "attachments": extract_field(r"Attachments[:\s]*([^\n]+)", text),
        "initialEstimate": extract_field(r"Initial Estimate[:\s]*([0-9,]+)", text),
    })


    acord = {
        "policyNumber": fields.get("policyNumber") or extract_field(r"POLICY\s*NUMBER[:\s]*([A-Za-z0-9\-]+)", text),

        "policyholderName": fields.get("policyholderName") or extract_field(
            r"NAME\s+OF\s+INSURED[:\s]*([A-Za-z0-9 ,\.]+)", text
        ),

        "incidentDate": fields.get("incidentDate") or extract_field(
            r"DATE\s+OF\s+LOSS\s+AND\s+TIME[:\s]*([A-Za-z0-9\/\-\s:]+)", text
        ),

        "location": fields.get("location") or extract_field(
            r"LOCATION\s+OF\s+LOSS[:\s]*([^\n]+)", text
        ),

        "description": fields.get("description") or extract_field(
            r"DESCRIPTION\s+OF\s+ACCIDENT[:\s]*([\s\S]*?)(?:INSURED VEHICLE|OTHER VEHICLE|$)", text
        ),

    
        "assetID": fields.get("assetID") or extract_field(r"V\.?I\.?N\.?[:\s]*([A-Za-z0-9]+)", text),
        "assetType": fields.get("assetType") or extract_field(r"MAKE[:\s]*([A-Za-z0-9]+)", text),
        "model": extract_field(r"MODEL[:\s]*([A-Za-z0-9]+)", text),
        "year": extract_field(r"YEAR[:\s]*([0-9]{4})", text),

        "estimatedDamage": fields.get("estimatedDamage") or extract_field(
            r"ESTIMATE\s+AMOUNT[:\s]*([0-9,\.]+)", text
        ),
        "damageDescription": extract_field(
            r"DESCRIBE\s+DAMAGE[:\s]*([\s\S]*?)(?:ESTIMATE|WHEN CAN|$)", text
        ),
    }

    for k, v in acord.items():
        if v:
            fields[k] = v


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

