from __future__ import annotations
import math
from typing import Tuple, Iterable

Vec3 = Tuple[float, float, float]

def v_add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def v_sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def v_scale(a: Vec3, s: float) -> Vec3:
    return (a[0]*s, a[1]*s, a[2]*s)

def v_dot(a: Vec3, b: Vec3) -> float:
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def v_cross(a: Vec3, b: Vec3) -> Vec3:
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def v_len(a: Vec3) -> float:
    return math.sqrt(v_dot(a, a))

def v_unit(a: Vec3) -> Vec3:
    L = v_len(a)
    if L == 0: 
        return (0.0, 0.0, 0.0)
    return (a[0]/L, a[1]/L, a[2]/L)

def v_rotate_about_axis(v: Vec3, axis: Vec3, deg: float) -> Vec3:
    """Rodrigues rotation: rotate v around 'axis' (unit or not) by 'deg' degrees."""
    a = v_unit(axis)
    theta = math.radians(deg)
    cos_t = math.cos(theta)
    sin_t = math.sin(theta)
    # v_parallel = (v·a) a
    dot_va = v_dot(v, a)
    v_par = v_scale(a, dot_va)
    # v_perp = v - v_parallel
    v_perp = v_sub(v, v_par)
    # a × v_perp
    a_cross_vperp = v_cross(a, v_perp)
    # Rodrigues
    term1 = v_par
    term2 = v_scale(v_perp, cos_t)
    term3 = v_scale(a_cross_vperp, sin_t)
    return v_add(term1, v_add(term2, term3))