# main.py
import os
from documentreader import read_doc
from extractor import extract_fields
from rules import apply_rules
from json_writer import write_output


def process_fnol(path):
    text = read_doc(path)
    fields = extract_fields(text)
    route, missing, reasons = apply_rules(fields)
    output = {
        "extractedFields": fields,
        "missingFields": missing,
        "recommendedRoute": route,
        "reasoning": "; ".join(reasons),
    }
    filename = os.path.splitext(os.path.basename(path))[0]
    out_path = write_output(output, filename)
    print(f"Processed {path} -> {out_path}")


if __name__ == "__main__":
    folder = "sampledocs"
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        if os.path.isfile(fpath) and (fpath.endswith(".txt") or fpath.endswith(".pdf")):
            try:
                process_fnol(fpath)
            except Exception as e:
                print(f"Error processing {fname}: {e}")
