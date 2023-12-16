import math


def v_prod(pt1, pt2, pt3, pt4):
    v1 = (pt2[0] - pt1[0], pt2[1] - pt1[1])
    v2 = (pt4[0] - pt3[0], pt4[1] - pt3[1])
    return v1[0] * v2[1] - v1[1] * v2[0]


def check_intersection(seg1, seg2):
    pt_a, pt_b = seg1
    pt_c, pt_d = seg2
    st1 = v_prod(pt_a, pt_b, pt_a, pt_c) * v_prod(pt_a, pt_b, pt_a, pt_d) < 0
    st2 = v_prod(pt_c, pt_d, pt_c, pt_a) * v_prod(pt_c, pt_d, pt_c, pt_b) < 0
    return st1 and st2


def intersect_pol_seg(polygon, segment):
    found = False
    first = polygon[0]
    prev = polygon[0]
    for elem in polygon():
        found = check_intersection((prev, elem), segment)
        prev = elem
        if found:
            return True
    if check_intersection((first, polygon[len(polygon) - 1]), segment):
        return True
    return False
