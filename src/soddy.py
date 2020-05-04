#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`soddy` module

:author: `Irevoire - Hetoxys <http://portail.fil.univ-lille1.fr>`_

:date:  2015 - 2016
"""

import points as pt
import circles as cir
import math
import cmath

def __is_outer_circle(C, cA, cB):
    """
    Checks if circle C contains circles cA and cB.

    :param C: The circle to test
    :type C: Circle
    :param cA: A circle
    :type cA: Circle
    :param cB: A circle
    :type cB: Circle
    """
    C_center, C_radius = cir.get_center(C), cir.get_radius(C)
    if pt.dist(C_center, cir.get_center(cA)) > C_radius:
        return False
    elif pt.dist(C_center, cir.get_center(cB)) > C_radius:
        return False
    else:
        return True

def descartes_curvature (c1, c2, c3):
    """
    :param c1:
    :type c1: circle
    :param c2:
    :type c2: circle
    :param c3:
    :type c3: circle
    """
    r1, r2, r3 = cir.get_radius(c1), cir.get_radius(c2), cir.get_radius(c3)
    if __is_outer_circle(c1, c2,c3):
        k1, k2, k3 = -1/r1, 1/r2, 1/r3     ## Si il y a un cercle qui contient les deux autres alors on lui met une "curvature" négative
    elif __is_outer_circle(c2, c1,c3):
        k1, k2, k3 = 1/r1, -1/r2, 1/r3
    elif __is_outer_circle(c3, c1,c2):
        k1, k2, k3 = 1/r1, 1/r2, -1/r3
    else:
        k1, k2, k3 = 1/r1, 1/r2, 1/r3
    a = k1 + k2 + k3
    b = 2*math.sqrt(k1*k2 + k1*k3 + k2*k3)
    return (k1, k2, k3, (a+b, a-b))

def descartes_center (k1, k2, k3, k4, z1, z2, z3):             ## Le centre des cercles
    """
    k1, k2, k3, k4 must be found with the :func:`descartes` function.
    z1, z2, z3 : The center of the 3 circle

    :param ki:
    :type ki: float
    :param zi:
    :type zi: point
    :return: The center of the two circle plus some random points
    :rtype: tuples
    """
    A = z1*k1 + z2*k2 + z3*k3
    B = 2 * cmath.sqrt(k1*k2*z1*z2 + k1*k3*z1*z3 + k2*k3*z2*z3)
    return ((A+B)/k4[0], (A-B)/k4[0], (A+B)/k4[1], (A-B)/k4[1])

def soddy (c1, c2, c3) :
    """
    :param c1:
    :type c1: circle
    :param c2:
    :type c2: circle
    :param c3:
    :type c3: circle
    :return: A list of length 2 wich contain the great circle in first and the small circle
    :rtype: list
    """
    k1, k2, k3, k4 = descartes_curvature(c1, c2, c3)
    Tcenter = descartes_center(k1, k2, k3, k4, cir.get_center(c1), cir.get_center(c2), cir.get_center(c3))  ## The tuple wich contain all the center
    k4 = (math.fabs(k4[0]), math.fabs(k4[1]))
    sm_circle, gr_circle = [], []
    margin = 1e-5
    if 1/k4[0] < 1/k4[1]:
        rad_sm_cir, rad_gr_cir = 1/k4[0], 1/k4[1]  ## radius small, great circle (28.71, 399.99)
    else:
        rad_gr_cir, rad_sm_cir = 1/k4[0], 1/k4[1]
    for c in Tcenter :
        small_counter, great_counter = 0, 0
        for circle in [c1, c2, c3] :
            radius_circle = cir.get_radius(circle)
            dist_center = pt.dist(c, cir.get_center(circle))
            if math.fabs(dist_center - (rad_sm_cir + radius_circle)) < margin:
                small_counter +=1                                           ## Si un cercle est tangent au cercle candidat-solution
            if math.fabs(dist_center - (rad_gr_cir - radius_circle)) < margin\
                or math.fabs(dist_center - (rad_gr_cir + radius_circle)) < margin:
                great_counter += 1
        if small_counter == 3 :
            sm_circle.append(c)  ## Si les trois cercles sont tangent au cercle candidat-solution alors on ajoute sont centre a la liste
        if great_counter == 3 :
            gr_circle.append(c)
    return [cir.make_circle(sm_circle[0], rad_sm_cir), cir.make_circle(gr_circle[0], rad_gr_cir)]

def small_soddy (c1, c2, c3) :
    """
    Return only the small

    :param c1:
    :type c1: circle
    :param c2:
    :type c2: circle
    :param c3:
    :type c3: circle
    :return: The small circle
    :rtype: circle
    """
    k1, k2, k3, k4 = descartes_curvature(c1, c2, c3)
    Tcenter = descartes_center(k1, k2, k3, k4, cir.get_center(c1), cir.get_center(c2), cir.get_center(c3))  ## The tuple wich contain all the center
    k4 = (math.fabs(k4[0]), math.fabs(k4[1]))
    sm_circle, gr_circle = [], []
    margin = 1e-8
    if 1/k4[0] < 1/k4[1]:
        rad_sm_cir= 1/k4[0]
    else:
        rad_sm_cir = 1/k4[1]
    for c in Tcenter :
        small_counter = 0
        for circle in [c1, c2, c3] :
            radius_circle = cir.get_radius(circle)
            dist_center = pt.dist(c, cir.get_center(circle))
            if math.fabs(dist_center - (radius_circle + rad_sm_cir)) < margin \
            or math.fabs(dist_center - (radius_circle - rad_sm_cir)) < margin :
                small_counter += 1
        if small_counter == 3 :
            sm_circle.append(c)
    return cir.make_circle(sm_circle[0], rad_sm_cir)
