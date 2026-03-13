"""
OPE-IsoGen Pipeline Attribute Codes
-----------------------------------
This file defines all numeric attribute codes used in the
coordinate-based pipeline data file.

These codes remain stable across the project and map directly
to values parsed from simple pipeline text files such as:

    100 1001=100 1004=500 10004=0 10005=0 10006=0 10007=0 10008=500 10009=0

This structure mimics a simplified PCF/IDF style numeric format.
"""

# --------------------------------------------------------------
# Component Types
# --------------------------------------------------------------
TYPE     = 1000      # Component type

PIPE     = 100       # Straight pipe segment
ELBOW    = 101       # Elbow/bend (45° or 90°, CLR required)

# --------------------------------------------------------------
# Dimensional Attributes
# --------------------------------------------------------------
OD       = 1001      # Outside diameter
LENGTH   = 1004      # Pipe length (optional when coordinates provided)
ANGLE    = 1005      # Elbow angle (45 / 90)
CLR      = 1006      # Elbow centerline radius (R)

# --------------------------------------------------------------
# Tangent / Coordinate Attributes
# --------------------------------------------------------------
# NOTE:
# These represent absolute 3D centerline coordinates.
P0_X    = 10001
P0_Y    = 10002
P0_Z    = 10003

START_X  = 10004
START_Y  = 10005
START_Z  = 10006

END_X    = 10007
END_Y    = 10008
END_Z    = 10009

MID_X    = 10010
MID_Y    = 10011
MID_Z    = 10012

# --------------------------------------------------------------
# Useful Collections
# --------------------------------------------------------------
COORD_START_KEYS = (START_X, START_Y, START_Z)
COORD_END_KEYS   = (END_X, END_Y, END_Z)
COORD_MID_KEYS   = (MID_X, MID_Y, MID_Z)
COORD_P0_KEYS    = (P0_X, P0_Y, P0_Z)

COMPONENT_TYPES = {
    PIPE:  "PIPE",
    ELBOW: "ELBOW",
}