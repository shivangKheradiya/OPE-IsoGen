# pipeline/parser.py
from .attribute_codes import COMPONENT_TYPES, ATTR_CODES, SKEY

def parse_pipeline_file(path: str):
    items = []

    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            # Split fields by whitespace
            parts = line.split()
            if len(parts) < 1:
                continue

            # First field must be numeric component code
            try:
                comp_code = int(parts[0])
            except ValueError:
                continue

            entry = {1000: comp_code}               # TYPE
            entry[1014] = SKEY.get(comp_code, "")   # SKEY auto

            # Parse attributes like: 1001=100
            for seg in parts[1:]:
                if "=" not in seg:
                    continue
                attr, val = seg.split("=", 1)
                try:
                    attr = int(attr)
                except ValueError:
                    continue

                try:
                    val = float(val)
                except ValueError:
                    pass  # store string later if needed

                entry[attr] = val

            items.append(entry)

    return items