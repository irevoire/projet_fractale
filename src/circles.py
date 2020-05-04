#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`circle` module

:author: `Irevoire - Hetoxys <http://portail.fil.univ-lille1.fr>`_

:date:  2015 - 2016

This module implements some functions to create a circle and get his radius or center.

To create a circle you must ;

* create a point with :func:`points.make_point`
* and create yout circle with :func:`make_circle`

To get his caracteristics ;

* You can get his center with :func:`get_center`
* You can get his radius with :func:`get_radius`
"""

def make_circle (center, radius):
    """
    creates a circle of center `center` and radius `radius`

    :param center:
    :type center: point
    :param radius:
    :type radius: int
    :Example:

    >>> import points
    >>> center = points.make_point(50, 50)
    >>> circle = make_circle(center, 25)
    """
    return {"center" : center,
            "radius" : radius}

def get_center (circle):
    """
    :param circle: a circle
    :type circle: circle
    :return: the center of the circle
    :rtype: center
    :UC: none
    :Example:

    >>> import points
    >>> center = points.make_point(50, 50)
    >>> circle = make_circle(center, 25)
    >>> get_center(circle) == center
    True
    """
    return circle["center"]

def get_radius (circle):
    """
    :param circle: a circle
    :type circle: circle
    :return: the radius of the circle
    :rtype: int
    :UC: none
    :Example:

    >>> import points
    >>> center = points.make_point(50, 50)
    >>> circle = make_circle(center, 25)
    >>> get_radius(circle)
    25
    """
    return circle["radius"]
