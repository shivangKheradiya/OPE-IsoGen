from .attribute_codes import COMPONENT_TYPES
from ..symbols2d.pipe import StraightPipe2D, StraightPipe2DParams
from ..symbols2d.elbow import Elbow2D, ElbowParams
from ..connect.engine import connect_parent_child


def make_symbol(item):
    comp = int(item[1000])  # numeric type

    if comp == COMPONENT_TYPES["PIPE"]:
        return StraightPipe2D(StraightPipe2DParams(
            od_mm=item.get(1001, 100.0),
            length_mm=item.get(1004, 500.0)
        ))

    if comp == COMPONENT_TYPES["ELBOW"]:
        return Elbow2D(ElbowParams(
            od_mm=item.get(1001, 100.0),
            angle_deg=item.get(1005, 90.0),
            radius_mm=item.get(1006, None)
        ))

    # TODO: reducers, tees, valves...

    return None


def generate_from_items(items, plane="XY"):
    if not items:
        return [], []

    # Start with first component
    parent = make_symbol(items[0])
    prims, markers = parent.place_iso(plane, rot_deg=0.0, at=(0,0), add_markers=True)

    # Chain next components
    current = parent

    for item in items[1:]:
        child = make_symbol(item)
        cp, cm = connect_parent_child(current, child, plane=plane)
        prims.extend(cp)
        markers.extend(cm)
        current = child

    return prims, markers


def generate_from_file(path, plane="XY"):
    from .parser import parse_pipeline_file
    items = parse_pipeline_file(path)
    return generate_from_items(items, plane=plane)