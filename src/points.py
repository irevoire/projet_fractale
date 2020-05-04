#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`points` module

:author: `Irevoire - Hetoxys <http://portail.fil.univ-lille1.fr>`_

:date:  2015 - 2016

This module implements some functions to create a point and get his coordinates.

To create a point, one has to:

* use :func:`make_point`

To get his caracteristics ;

* get his abscissa with :func:`get_abs`
* get his ordinate with :func:`get_ord`

"""

import math

def make_point (x, y):
    """
    Creates a point of coordinates (x,y)

    :param x:
    :type x: int
    :param y:
    :type y: int
    """
    return complex(x, y)

def get_abs (point):
    """
    :param point: a point
    :type point: point
    :return: The abscissa of the point
    :rtype: int
    :UC: none
    :Example:

    >>> point = make_point(200, 100)
    >>> get_abs(point)
    200
    """
    return point.real

def get_ord (point):
    """
    :param point: a point
    :type point: point
    :return: The ordinate of the point
    :rtype: int
    :UC: none
    :Example:

    >>> point = make_point(200, 100)
    >>> get_ord(point)
    100
    """
    return point.imag

def dist(pt1, pt2) :
    """
    :Example:

    >>> dist((10+10j), (5+5j))
    5.0
    >>> dist((5+10j), (5+0j))
    10.0
    """
    return math.sqrt((get_abs(pt1) - get_abs(pt2))**2 + (get_ord(pt1) - get_ord(pt2))**2)
