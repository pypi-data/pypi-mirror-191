#!/usr/bin/python3
"""
t5html converts a t5html-formatted file into HTML

USAGE:

    t5html filename
"""
from . import readfile, make_html

import sys

example = """
## t5html

DOCTYPE := <!DOCTYPE html>

!! DOCTYPE

!! <-- This is
.. a html comment
.. over multiple lines -->

html
   head
   body
      div#id.cls1.cls2 attr1=value1 attr2="some quoted value"
         article#id > p > "textnode
            .. over multiple
            .. lines
            section
               p#id1 | p#id2 | p#id3
               p#id4 > "Text Node < p#id5
               p#id6
                  "Text Node
"""

def start():
    """
    entry point
    """
    if len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        from . import VERSION
        title = f"T5HTML v({VERSION})"
        print(title)
        exit(__doc__ + "\n\nERROR: Seems like we didn't get a filename")


    input = readfile(fname)
    print(make_html(input))


if __name__ == "__main__":
    start()


# vi: set et ts=4 ts=4 ai cc=78 nowrap nu so=5:
