# Central place to manage debugging flags for geometry output
# More flags can be added later (dimensions, bounding boxes, normals, etc.)

class DebugFlags:
    # Turn on/off coordinate labels in SVG output
    SHOW_COORDINATES = True

    # Show component names (PIPE, ELBOW) next to geometry
    SHOW_COMPONENT_LABELS = False

    # Show internal tangent points for elbows
    SHOW_TANGENT_POINTS = True

    # Show global 3D routing path (projected polyline)
    SHOW_3D_ROUTE = False

debug = DebugFlags()