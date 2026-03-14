from __future__ import annotations
import math

def is_zero(val: float, tol: float = 1e-9) -> bool:
    return abs(val) <= tol

def wrap_angle_rad(a: float) -> float:
    """Wrap angle to (-pi, pi]."""
    a = math.fmod(a, 2*math.pi)
    return a - 2*math.pi if a <= -math.pi else (a - 2*math.pi if a > math.pi else a)
