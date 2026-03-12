"""
============================================================
  PCF / IDF - STYLE MASTER ATTRIBUTE TABLE (NUMERIC CODES)
============================================================

This file defines the official numeric codes used across the
entire OPE-IsoGen engine.

Why numeric codes?
------------------
Following PCF/IDF conventions, numeric codes ensure:
 - consistent internal attribute mapping
 - extremely fast processing
 - robust component identification
 - easy future compatibility with CAESAR II, E3D, PDMS, IDF, ISOGEN
 - no issues with case sensitivity or renamed attributes

Structure
---------
100-199     Component Type Codes (PCF-like)
1000-1999   Common Piping Attributes (PCF / IDF compatible)
2000-2999   OPE-IsoGen Internal Attributes (YOUR custom range)
3000-3999   Future CAD Export Attributes (DXF/STEP special)
 
============================================================
"""

# ----------------------------------------------------------
# COMPONENT TYPE CODES (100-199)
# ----------------------------------------------------------
# These correspond to piping components. They match the
# PCF/IDF convention of using a numeric COMPONENT-ID.
# ----------------------------------------------------------

COMPONENT_TYPES = {
    "PIPE":     100,    # Straight pipe spool piece
    "ELBOW":    101,    # Butt-weld elbow (45°/90°)
    "REDUCER":  102,    # Concentric / Eccentric reducer
    "TEE":      103,    # Tee (equal/unequal)
    "VALVE":    104,    # Valve (gate, ball, check, etc.)
    "FLANGE":   105,    # Flange (slip-on, weld neck, etc.)
    "CAP":      106,    # End cap
    "SUPPORT":  107,    # Pipe support (shoes, guides, etc.)
}

# Default SKEY mapping (Isometric symbols)
SKEY = {
    100: "PIPE",
    101: "ELBW",
    102: "RED",
    103: "ET",
    104: "VALVE",
    105: "FLG",
    106: "CAP",
    107: "SUP",
}


# ----------------------------------------------------------
# COMMON ATTRIBUTE CODES (1000-1999)
# ----------------------------------------------------------
# These attribute numbers follow PCF/IDF naming style.
# Each attribute is assigned a numeric key. Internal data
# always uses these codes (never raw text).
# ----------------------------------------------------------

ATTR_CODES = {

    # ---- Pipe Dimensions ----
    "OD": 1001,              # Outside Diameter (mm)
    "ID": 1002,              # Inside Diameter (mm)
    "THK": 1003,             # Wall Thickness (mm)
    "LENGTH": 1004,          # Centerline Length (mm)
    "LEN": 1004,             # Alias for LENGTH

    # ---- Elbow / Bending ----
    "ANGLE": 1005,           # Elbow angle (45 or 90)
    "CLR": 1006,             # Centerline Radius of elbow (mm)

    # ---- Reducer ----
    "OD1": 1007,             # Inlet OD
    "OD2": 1008,             # Outlet OD

    # ---- Tee ----
    "BRANCH_OD": 1009,       # Branch outside diameter

    # ---- Flange / Valve ----
    "RATING": 1010,          # Pressure rating e.g. 150, 300
    "FACE": 1011,            # Flange face (RF, FF, RTJ)
    "VALVE_TYPE": 1012,      # Valve type code (Gate=1, Ball=2, Check=3)

    # ---- Orientation / Special ----
    "ORIENTATION": 1013,     # Branch orientation (N,S,E,W)
    "SKEY": 1014,            # Symbol key (ELBW, RED, etc.)
}


# ----------------------------------------------------------
# OPE-ISOGEN CUSTOM INTERNAL ATTRIBUTE RANGE (2000-2999)
# ----------------------------------------------------------
# This range is reserved exclusively for your future
# isometric generator needs.
# Add any custom internal fields here (never conflict with
# PCF/IDF namespace).
# ----------------------------------------------------------

OPE_ISOGEN_CODES = {
    "SYM_VERSION": 2000,         # Version of symbol definition
    "GRAPHIC_STYLE": 2001,       # Drafting style (simple, detailed, iso)
    "FLOW_DIRECTION": 2002,      # Flow direction override
    "DIM_STYLE": 2003,           # Dimension style code
    "ANNOTATION": 2004,          # Any extra annotation
    "USER_FLAG1": 2005,          # Custom usage
    "USER_FLAG2": 2006,          # Custom usage
}


# ----------------------------------------------------------
# FUTURE CAD EXPORT RANGE (3000-3999)
# ----------------------------------------------------------
# Reserved for DXF/STEP/IGES export-specific properties.
# ----------------------------------------------------------

CAD_EXPORT_CODES = {
    "LAYER": 3000,           # Target CAD layer name/ID
    "COLOR": 3001,           # CAD color index
    "LINESTYLE": 3002,       # CAD linestyle
}
