#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
:mod:`fractals` module

:author: `Irevoire - Hetoxys <http://portail.fil.univ-lille1.fr>`_

:date:  2015 - 2016

This module implements some functions to create a circle crown and a fractal of circle crown.


.. topic:: This module uses functions from : :mod:`points`,  :mod:`circles` and :mod:`soddy` :


    #. From :mod:`points` :
        * :func:`points.make_point`
        * :func:`points.get_abs`
        * :func:`points.get_ord`
    #. From :mod:`circles` :
        * :func:`circles.make_circle`
        * :func:`circles.get_center`
        * :func:`circles.get_radius`
    #. From :mod:`soddy` :
        * :func:`soddy.soddy`
        * :func:`soddy.small_soddy`

Functions :
===========
"""

import sys
import circles  as cir
import points   as pt
import soddy    as so
import math
import random
import time

color_list = ['white']


#####################################
## Fonctions de dessin des cercles ##
#####################################


def draw_circle (circle, outline="black"):
    """
    :param circle:
    :type circle: circle
    :Action: draw a circle in the Tkinter's canvas
    """
    global candim
    left   = pt.get_abs(cir.get_center(circle)) - cir.get_radius(circle)
    top    = pt.get_ord(cir.get_center(circle)) - cir.get_radius(circle)
    right  = pt.get_abs(cir.get_center(circle)) + cir.get_radius(circle)
    bottom = pt.get_ord(cir.get_center(circle)) + cir.get_radius(circle)
    if save_frac :
        draw.ellipse((left, top, right, bottom), outline="black")
    else :
        can.create_oval(left, top, right, bottom, width=1, outline = outline, fill=random.choice(color_list))

def Ldraw_circle(Lcircle):
    """
    :param Lcircle: The circles you want to draw
    :type Lcircle: list
    :Action: Draw all the circles in the list
    :UC: Lcircle must contain only circle elements
    """
    for i in Lcircle :
        draw_circle(i)

#########################
## Couronne de cercles ##
#########################


def __find_radius (circle, n):
    """
    :param circle: The great circle
    :type circle: circle
    :param n: Number of circle
    :type n: int
    :return: A tuple wich contains first the radius of the "crown" of circles and the radius of the inner circle.
    :rtype: tuple
    """
    radius = cir.get_radius(circle)
    return (  radius * ( math.sin(math.pi/n) / (1 + math.sin(math.pi/n))),                  ## radius of the "crown" of circle
              radius * (( 1 - math.sin(math.pi/n)) / (1 + math.sin(math.pi/n)))  )          ## radius of the "inner" circle

def __find_points (center, n, radius):
    """
    :param n: Number of circle
    :type n: int
    :param radius: The radius of the "crown" of circle and of the inner circle
    :type radius: tuple
    :return: A list wich contain the center of all the circle of the "crown"
    :rtype: list
    :UC: The radius of the inner circle must be the last of the tuple
    and len(radius) = 2
    """
    r, r1 = radius[1], radius[0]
    return [( pt.make_point((r + r1) * math.cos(2*i*math.pi/n) + pt.get_abs(center)  ,  (r + r1) * math.sin(2*i*math.pi/n) + pt.get_ord(center)))    for i in range(n)]

def make_crown (circle, n):
    """
    Create a list of circle.

    :param circle: The first circle wich contain all the other
    :type circle: circle
    :param n: The number of circles you want to put inside the first circle
    :type n: int
    :return: A list of circles, the last circle is the inner circle, all the other are the crown
    :rtype: list
    """
    radius = __find_radius(circle, n)
    points = __find_points(cir.get_center(circle), n, radius)
    return [circle, cir.make_circle( cir.get_center(circle), radius[1]) ] + [  cir.make_circle(i, radius[0]) for i in points  ]

def crown(x, y, radius, nb_circle = 5):
    """
    Draw a circle of center `x, y` and radius `radius` and the crown inside.

    :param x: abs
    :type x: int
    :param y: ord
    :type y: int
    :param radius: -
    :type radius: int
    :Action: Draw a crown of circles inside the center of center `x, y` and radius `radius`.
    """
    center = pt.make_point(x, y)
    circle = cir.make_circle(center, radius)
    draw_circle(circle)
    Ldraw_circle(make_crown(circle, nb_circle))

def fractal_crowns(x, y, radius, depth = 5, nb_circle = 0):
    """
    Creates a circle of center `x, y` and radius `radius` and the crown inside.
    If you let the default value on `nb_circle` the number of circle in every depth of the fractal will be random.

    :param x: abs
    :type x: int
    :param y: ord
    :type y: int
    :param radius: -
    :type radius: int
    :param depth: (Default value : 5)  The depth of the fractal
    :type depth: int
    :param nb_circle: (Default value : Random)  The number of circles the crown contain
    :type nb_circle: int
    :Action: Draw the fractal `crown` of circles inside the center of center `x, y` and radius `radius`.
    :UC: radius, depth, nb_circle must be positive integers.
    """
    assert type(depth) == type(nb_circle) == int, "depth and nb_circle must be integers"
    assert radius > 0 and depth > 0 and nb_circle > 0, "radius, depth and nb_circle must be positive"
    nb_circle2 = 0
    if nb_circle == 0 :
        nb_circle = random.randint(0, depth) + 3
        nb_circle2 = 1
    if depth != 0 :
        center = pt.make_point(x, y)
        circle = cir.make_circle(center, radius)
        draw_circle(circle)
        Lcrowns = make_crown(circle, nb_circle)
        Ldraw_circle(Lcrowns)
        for c in Lcrowns :
            point = cir.get_center(c)
            x, y = pt.get_abs(point), pt.get_ord(point)
            if nb_circle2 :
                nb_circle = 0
            fractal_crowns(x, y, cir.get_radius(c), depth - 1, nb_circle)

## Apollonius ##

def soddy_fract(L, c1, c2, c3, depth):
    """
    Fills the space between 3 circles with the apollonius fractal

    :param L: A list generate with the :func:`make_crown` function
    :type L: list
    :param depth: The depth of the fractal
    :type depth: int
    :Action: add the new circle at the end of the list L
    """
    if depth != 0 and cir.get_radius(c1)>0.5 and cir.get_radius(c2)>0.5 and cir.get_radius(c3)>0.5 :
        try :
            circle = so.small_soddy(c1, c2, c3)
            L += [circle]
            soddy_fract(L, circle, c2, c3, depth - 1)
            soddy_fract(L, c1, circle, c3, depth - 1)
            soddy_fract(L, c1, c2, circle, depth - 1)
        except : raise

def apollonius(L, depth):
    """
    Fills a crown with the apollonius fractal

    :param L: A list generate with the :func:`make_crown` function
    :type L: list
    :param depth: The depth of the fractal
    :type depth: int
    """
    lenL = len(L)
    soddy_fract(L, L[0], L[lenL-1], L[2], depth)
    soddy_fract(L, L[1], L[lenL-1], L[2], depth)
    for i in range(2, lenL - 1):
        soddy_fract(L, L[0], L[i], L[i+1], depth)
        soddy_fract(L, L[1], L[i], L[i+1], depth)

#####################
## Fonction finale ##
#####################

def __same_circle(cA,cB):  ## Pour l'instant inutilisée
    if pt.dist(cir.get_center(cA), cir.get_center(cB)) > 1e-5:
        return False
    elif maht.fabs(cir.get_radius(cA) - cir.get_radius(cB)) > 1e-5:
        return False
    else:
        return True

def final(x, y, radius, apo_depth = 5, crown_depth = 1, nb_circle = 3):
    """
    :param x: The center of first circle
    :type x: int
    :param y: The center of first circle
    :type y: int
    :param radius: The radius of the first circle
    :type radius: int
    :param depth: The depth of the fractal
    :type depth: int
    :param nb_circle: The number of circle in the crown
    :type nb_circle: int
    :Action: Draw the Apollonius Badern.
    :UC: radius, depth, nb_circle must be positive integers.
    """
    global Gcrowndepth
    global Gnb_circle
    if Gnb_circle == 0 :
        nb_circle = random.randint(3, 10)
        crown_depth = random.randint(0, 2)
        apo_depth = random.randint(0, 2)
    else : nb_circle = Gnb_circle
    if crown_depth != 0 and radius > 1:
        center = pt.make_point(x, y)
        circle = cir.make_circle(center, radius)
        Lcrowns = make_crown(circle, nb_circle)
        apollonius(Lcrowns, apo_depth)
        draw_circle(Lcrowns[0])
        Lcrowns = Lcrowns[1:]
        while Lcrowns != [] and radius > 1:
            if Gcrown_depth == crown_depth and len(Lcrowns)%100 == 0 :
                print(len(Lcrowns))  ## Donne une idée de l'avancement du programme
            c = Lcrowns[0]
            x1 = pt.get_abs(cir.get_center(c))
            y1 = pt.get_ord(cir.get_center(c))
            draw_circle(c)
            final(x1, y1, cir.get_radius(c), apo_depth, crown_depth - 1, nb_circle)
            Lcrowns = Lcrowns[1:]


##################################
#######        TESTS       #######
##################################

#final(350, 350, 300, 15)

##point = pt.make_point(350, 350)
##circle = cir.make_circle(point, 300)
##crown = make_crown(circle, 5)
##Ldraw_circle(crown)

## Cas avec trois cercles de même rayon
#Ldraw_circle([{'center': (614.3593539448982+400j), 'radius': 185.64064605510183},{'center': (292.82032302755096+585.6406460551018j), 'radius': 185.64064605510183},{'center': (292.8203230275508+214.3593539448982j), 'radius': 185.64064605510183}])
#Ldraw_circle(so.soddy({'center': (614.3593539448982+400j), 'radius': 185.64064605510183},{'center': (292.82032302755096+585.6406460551018j), 'radius': 185.64064605510183},{'center': (292.8203230275508+214.3593539448982j), 'radius': 185.64064605510183}))

## Cas avec deux cercles de même rayon et un petit cercle
#Ldraw_circle([{'center': (292.82032302755096+585.6406460551018j), 'radius': 185.64064605510183},{'center': (292.8203230275508+214.3593539448982j), 'radius': 185.64064605510183},{'center': (400+400j), 'radius': 28.71870788979634}])
#draw_circle(so.small_soddy({'center': (292.82032302755096+585.6406460551018j), 'radius': 185.64064605510183},{'center': (292.8203230275508+214.3593539448982j), 'radius': 185.64064605510183},{'center': (400+400j), 'radius': 28.71870788979634}))

#L = [{'radius': 200, 'center': (200+200j)}, {'radius': 74.03838163175003, 'center': (98.09491010111422+125.96161836824999j)}, {'radius': 74.03838163175003, 'center': (238.92428071476076+80.20338204779254j)}]
#Ldraw_circle(L)
#draw_circle(so.small_soddy({'radius': 200, 'center': (200+200j)}, {'radius': 74.03838163175003, 'center': (98.09491010111422+125.96161836824999j)}, {'radius': 74.03838163175003, 'center': (238.92428071476076+80.20338204779254j)}))

## Cas avec deux cercles contenu dans un plus gros
#Ldraw_circle([{'radius': 400, 'center': (400+400j)}, {'radius': 185.64064605510183, 'center': (614.3593539448982+400j)}, {'radius': 185.64064605510183, 'center': (292.82032302755096+585.6406460551018j)}])
#draw_circle(so.small_soddy({'radius': 400, 'center': (400+400j)}, {'radius': 185.64064605510183, 'center': (614.3593539448982+400j)}, {'radius': 185.64064605510183, 'center': (292.82032302755096+585.6406460551018j)}))



#### Le main

save_frac = 0
execute = 1
candim = 0
Gapo_depth = 0
Gcrown_depth = 0
Gnb_circle = 0

def main():
    global save_frac
    global execute
    global candim
    global Gapo_depth
    global Gcrown_depth
    global Gnb_circle
    global save_frac
    if not (len(sys.argv) in (1, 5, 6))  :
        usage()
    else:
        try:
            if len(sys.argv) == 1 :
                candim = 1000
                Gapo_depth = 1000
                Gcrown_depth = 2
                Gnb_circle = 5
                save_frac = 0
            elif len(sys.argv) == 5 :
                candim = int(sys.argv[1])
                Gapo_depth = int(sys.argv[2])
                Gcrown_depth = int(sys.argv[3])
                Gnb_circle = int(sys.argv[4])
            elif len(sys.argv) == 6 :
                candim = int(sys.argv[1])
                Gapo_depth = int(sys.argv[2])
                Gcrown_depth = int(sys.argv[3])
                Gnb_circle = int(sys.argv[4])
                save_frac = sys.argv[5]
            assert (candim > 0) and (Gcrown_depth >= 1) and (Gapo_depth >= 0) and (Gnb_circle >= 3 or Gnb_circle == 0), "radius, depth and nb_circle must be positive"
        except:
            raise
            usage()


def usage():
    print("Usage : %s <Dimensions> <Apollonius Depth> <Crown Depth> <Number of circles> [save]"%sys.argv[0])
    print("<Dimensions> : The dimensions of the fractal. Must be a positive integer.")
    print("<Apollonius Depth> : The depth of the Apollonius fractal. Must be a positive integer.")
    print("<Crown Depth> : The depth of the crwn fractal. Must be a positive integer.")
    print("<Number of circles> The number of circles per crown. Must be > 3 integer.")
    print("[save] (optionnal) : If you want to save your drawing. Must be a string.")
    exit()

if __name__ == "__main__" :
    main()

if save_frac:
    try :
        from PIL import Image, ImageDraw
    except :
        execute = 0
        print("You need the :mod:PIL to save your fractal")
else :
    try :
        import tkinter as tk
    except :
        execute = 0
        print("You need :mod:tkinter to draw a fractal.")



if execute :
    if not save_frac:
        windo = tk.Tk()
        windo.title('Appollonius Fractals')
        can = tk.Canvas(windo,height=candim+4,width=candim+4, bg="white")
        can.pack()
    else:
        image = Image.new("RGB", (candim, candim), (255, 255, 255))
        draw = ImageDraw.Draw(image)
    try:
        final(candim/2 + 2, candim/2 + 2, candim/2, Gapo_depth, Gcrown_depth, Gnb_circle)
    except:
        usage()
    if save_frac:
        image.save(save_frac + ".png")
        print("Finished.")
    else:
        windo.mainloop()
