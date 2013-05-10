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

letters = translate_word(sys.argv[1])
print letters
