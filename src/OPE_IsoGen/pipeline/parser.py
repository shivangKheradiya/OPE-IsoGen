from __future__ import annotations
import json
from typing import List, Dict

"""
Two simple formats supported:

1) TXT line-based:
   PIPE, OD=100, L=500
   ELBOW90, OD=100, R=150
   PIPE, OD=100, L=300

2) JSON array:
   [
     {"type":"pipe","od":100,"length":500},
     {"type":"elbow90","od":100,"radius":150},
     {"type":"pipe","od":100,"length":300}
   ]
"""

def parse_pipeline_file(path: str) -> List[Dict]:
    if path.lower().endswith(".json"):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # TXT format
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            # Simple CSV-ish
            parts = [p.strip() for p in line.split(",")]
            if not parts: continue
            kind = parts[0].upper()
            item = {}
            if kind == "PIPE":
                item["type"] = "pipe"
            elif kind == "ELBOW90":
                item["type"] = "elbow90"
            else:
                continue
            # key=value pairs
            for seg in parts[1:]:
                if "=" in seg:
                    k,v = seg.split("=",1)
                    k = k.strip().lower()
                    v = v.strip()
                    try:
                        vnum = float(v)
                        item[k] = vnum
                    except ValueError:
                        item[k] = v
                else:
                    # ignore
                    pass
            out.append(item)
    return out