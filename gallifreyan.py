#!/usr/bin/env python

# Creates a 3D image of a word written in Circular Gallifreyan
#
# Written by Timur Tabi <timur@tabi.org>
# Copyright 2013 Timur Tabi
#
# See README.md for details and licensing information
#
# The Circular Gallifreyan alphabet is copyright Loren Sherman
#   http://www.shermansplanet.com/gallifreyan

import sys
import math
import Image, ImageDraw

ImageSize = 300

# Translates a single word into a list of Gallifreyan letters
# a b ch d e f g h i j k l m n ng o p qu r t th s sh u v w x y z
def translate_word(word):
    letters = []
    length = len(word)

    i = 0
    # Loop through the word, one letter at a time.  This is a look-ahead
    # algorithm, because we need to parse digraphs by looking at the next
    # letter, and converting both Latin letters into one Gallifreyan letter.
    #
    # We use a while-loop because when we parse a digraph, we want to skip a
    # letter, and we can't do that with a for-loop in Python.  The alternative
    # is to use a state machine, but this approach is simpler.
    #
    # Not that we always treat "ch", "ng", "qu", "sh", and "th", as digraphs.
    # That is, whenever we see "t" and "h" together, we assume it's the "th"
    # digraph.  This breaks with some words, like "lighthouse".
    while i < length:
        c = word[i]
        i += 1

        # First, deal with the easy letters
        if c in ['a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                 'o', 'p', 'r', 'u', 'v', 'w', 'x', 'y', 'z']:
            letters.append(c)
            continue

        # c2 is the next letter, if there is one
        c2 = word[i] if i < length else None

        # Test for digraphs
        if c == 'c':
            # There is no "c" in Gallifreyan, so either it's "ch", or we
            # replace it with "s" or "k"
            if c2 == 'h':
                # Does not work for words where "ch" is pronounced like "sh"
                letters.append('ch')
                i += 1
            elif c2 == 'k':
                # "ck" becomes "k".  This might be wrong.
                letters.append('k')
                i += 1
            elif c2 in ['a', 'o', 'u', 'l', 'r', None]:
                # assume it's a hard "c" if followed by any of these letters,
                # or it's at the end of the word
                letters.append('k')
            else:
                # Otherwise, assume it's a soft "c"
                letters.append('s')
        elif c == 'n':
            if c2 == 'g':
                # "ng" is not always a velar nasal, but we treat it like
                # one anyway.  Note that this conflicts with the Wiki, which
                # says that "change" should be "ch a n g e", but we treat it
                # as "ch a ng e"
                letters.append('ng')
                i += 1
            else:
                letters.append(c)
        elif c == 'q':
            if c2 == 'u':
                letters.append('qu')
                i += 1
            else:
                letters.append(c)
        elif c == 's':
            if c2 == 'h':
                letters.append('sh')
                i += 1
            else:
                letters.append(c)
        elif c == 't':
            if c2 == 'h':
                letters.append('th')
                i += 1
            else:
                letters.append(c)

    return letters

# enums for the various positions a circle can be in
POS_ON = 1      # On the inside rim
POS_IN = 2      # Completely inside the circle
POS_HALF = 3    # Half a circle on the inside rim
POS_THRU = 4    # A complete circle drawn through the rim

# The shape of the circle for the letter
letter_shapes = {
    'b':POS_ON,
    'ch':POS_ON,
    'd':POS_ON,
    'f':POS_ON,
    'g':POS_ON,
    'h':POS_ON,
    'j':POS_IN,
    'k':POS_IN,
    'l':POS_IN,
    'm':POS_IN,
    'n':POS_IN,
    'p':POS_IN,
    't':POS_HALF,
    'sh':POS_HALF,
    'r':POS_HALF,
    's':POS_HALF,
    'v':POS_HALF,
    'w':POS_HALF,
    'th':POS_THRU,
    'y':POS_THRU,
    'z':POS_THRU,
    'ng':POS_THRU,
    'qu':POS_THRU,
    'x':POS_THRU,
}

letter_dots = {
    'b':0,
    'ch':2,
    'd':3,
    'f':0,
    'g':0,
    'h':0,
    'j':0,
    'k':2,
    'l':3,
    'm':0,
    'n':0,
    'p':0,
    't':0,
    'sh':2,
    'r':3,
    's':0,
    'v':0,
    'w':0,
    'th':0,
    'y':2,
    'z':3,
    'ng':0,
    'qu':0,
    'x':0,
}

letter_lines = {
    'b':0,
    'ch':0,
    'd':0,
    'f':3,
    'g':1,
    'h':2,
    'j':0,
    'k':0,
    'l':0,
    'm':3,
    'n':1,
    'p':2,
    't':0,
    'sh':0,
    'r':0,
    's':3,
    'v':1,
    'w':2,
    'th':0,
    'y':0,
    'z':0,
    'ng':3,
    'qu':1,
    'x':2,
}

# Converts a list of Gallifreyan letters into a list of shapes
def make_shapes(word):
    return

# Returns the point on a circle (with center at 'center' and radius of
# 'radius') that is of angle 'angle' from the bottom, counter-clockwise.
# 'angle' is in degrees, where 0 points straight down, and increases
# counter-clockwise.
def position(center, radius, angle):
    d = math.radians(angle)
    cx = int(center + radius * math.sin(d))
    cy = int(center + radius * math.cos(d))

    return (cx, cy)

# Given two circles, one of radius r1 and the other of radius r2, where the
# senter of the second circle is of distance 'd' from the center of the first,
# return the angle (in degrees) of the intersection of the two circles.
#
# Imagine a line connecting the two centers.  The angle of intersection is
# the angle offset from this line to the intersections.
#
# The calculation of the intersecting points is taken from
# http://mathworld.wolfram.com/Circle-CircleIntersection.html
def angle_of_intersection(r1, r2, d):
    global Center

    print "r1 =", r1
    print "r2 =", r2
    print "d =", d
    x = (d**2 - r2**2 + r1**2) / (2*d)
    print "x =", x
    a = math.sqrt((-d + r2 - r1) * (-d - r2 + r1) * (-d + r2 + r1) * (d + r2 + r1)) / d
    print "a =", a
    return math.degrees(math.atan((a / 2) / (d - x)))

letters = translate_word(sys.argv[1].lower())
print letters

im = Image.new('1', (ImageSize, ImageSize))
draw = ImageDraw.Draw(im)

# How much indent from the each of the square to draw the word circle
Indent = ImageSize / 8

# The center point of the word circle
Center = ImageSize / 2

# The radius of the word circle
Radius = (ImageSize - 2 * Indent) / 2

# The number of degrees between each letter on the word circle
Arc = 360.0 / len(letters)

# The radius of the letter circles
Radius2 = ImageSize / 10

# The distance beyond the word circle of the center of the letter circle
# for letters that are half-circles
Extra = Radius2

draw.ellipse((Indent, Indent, ImageSize - Indent, ImageSize - Indent), outline="white")

for l in xrange(len(letters)):
    Angle = Arc * l
    if letter_shapes[letters[l]] == POS_IN:
        (cx, cy) = position(Center, Radius - (Radius2 + 10), Angle)
        draw.ellipse((cx - Radius2, cy - Radius2, cx + Radius2, cy + Radius2), outline="white")
    elif letter_shapes[letters[l]] == POS_ON:
        (cx, cy) = position(Center, Radius - Radius2, Angle)
        draw.ellipse((cx - Radius2, cy - Radius2, cx + Radius2, cy + Radius2), outline="white")
    elif letter_shapes[letters[l]] == POS_HALF:
        (cx, cy) = position(Center, Radius + Extra, Angle)
        Angle2 = (180 - Angle) + 90
        print "Angle2 =", Angle2
        Theta = angle_of_intersection(Radius, Radius2 * 2, Radius + Extra)
        print "Theta =", Theta
        print Angle2 - Theta, Angle2 + Theta
        Square = (cx - Radius2 * 2, cy - Radius2 * 2, cx + Radius2 * 2, cy + Radius2 * 2)
        draw.ellipse(Square, fill="black")
        draw.arc(Square, int(Angle2 - Theta), int(Angle2 + Theta), fill="white")
    elif letter_shapes[letters[l]] == POS_THRU:
        (cx, cy) = position(Center, Radius, Angle)
        draw.ellipse((cx - Radius2, cy - Radius2, cx + Radius2, cy + Radius2), outline="white")

im.show()
