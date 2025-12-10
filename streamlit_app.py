import streamlit as st
import os
import json
from documentreader import read_doc
from extractor import extract_fields
from rules import apply_rules

st.set_page_config(page_title="Insurance Claims Processing Agent", layout="wide")

st.title("📄 Autonomous Insurance Claims Processing Agent")
st.write(
    "Upload a PDF or TXT FNOL file to automatically extract fields and route the claim."
)

uploaded_file = st.file_uploader("Upload FNOL Document", type=["pdf", "txt"])

if uploaded_file:
    temp_path = "temp_uploaded_file." + uploaded_file.name.split(".")[-1]
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    try:
        text = read_doc(temp_path)
        fields = extract_fields(text)
        route, missing, reasons = apply_rules(fields)

        result = {
            "extractedFields": fields,
            "missingFields": missing,
            "recommendedRoute": route,
            "reasoning": "; ".join(reasons),
        }

        st.subheader("📌 Extracted Fields")
        st.json(fields)

        st.subheader("⚠️ Missing Fields")
        st.json(missing)

        st.subheader("🚦 Recommended Route")
        st.success(route)
        st.write(result["reasoning"])

        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="Download Output JSON",
            data=json_str,
            file_name="fnol_output.json",
            mime="application/json",
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")

    if os.path.exists(temp_path):
        os.remove(temp_path)
