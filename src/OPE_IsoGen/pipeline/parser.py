# src/OPE_IsoGen/pipeline/parser.py

from .attribute_codes import *

def parse_pipeline_file(path):
    items = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split()
            obj = {}
            obj[TYPE] = int(parts[0])

            for token in parts[1:]:
                if "=" not in token:
                    continue
                k, v = token.split("=")
                obj[int(k)] = float(v)

            items.append(obj)
    return items