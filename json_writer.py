# json_writer.py
import json, os


def write_output(output, filename):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    return path
