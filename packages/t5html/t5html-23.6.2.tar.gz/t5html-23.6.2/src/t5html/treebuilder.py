""" 
TreeBuilder

Creates a HTML-File from a t5html formatted file.
Utilizes the lineparser and elementparser modules.

Example:

    html = HTML_from_t5html(rawstr)

"""

from . import lineparser as lp
from . import elementparser as ep

import sys
from collections import namedtuple
from itertools import zip_longest


TreeElement = namedtuple("TreeElement", "level tag value orig_lnr")


def build_from_str(t5htmlstr):
    """
    takes a rawstr in t5html-format
    returns a list of LineStructures
    """
    return lp.parse_str(t5htmlstr)


def LineStructureFactory(src):
    """
    takes either a string or a list of LineStructures
    returns a list of LineStructures

    basically ensures that we have LineStructures independently if we are 
    fed a string in t5html format or already a converted list of
    LineStructures.
    """
    if type(src) == str:
        return build_from_str(src)
    elif type(src) == list and src and type(src[0]) == lp.LineStructure:
        # non empty list (`and src`) with 1st item of type LineStructure
        return src


def pseudoAST_from(structured_lines):
    """
    tales a list of linestructures
    returns a pseudoast
    """
    getvalue = lambda l: l.line.lstrip()\
                            if l.cls != 'element'\
                            else ep.parse_element(l.line.lstrip())
    return [ TreeElement(
                lp.get_indent_level(line.line),
                ep.element_name(getvalue(line)) if line.cls == 'element' else None,
                getvalue(line), 
                line.nr) for line in structured_lines]


def html_tree_from_ast(ast):
    """
    takes a (pseudo-)ast
    returns a list of formatted html lines
    """
    indentstr = lambda x: x*2*" "
    tree, tagstack = [], []
    for element, peek in zip_longest(ast, ast[1:], fillvalue=None):
        # this can cause errors for text-nodes with values like: "! some text 
        line = element.value.strip('"').strip('!') if not element.tag else element.value
        level = element.level
        if peek:
            if peek.level > element.level and element.tag and element.tag:
                # normal tag
                tagstack.append(element.tag)
            elif peek.level <= element.level and element.tag:
                # self-closing tag
                line = line[:-1] + '/>'

        tree.append(indentstr(level) + line)

        while peek and peek.level < level:
            # if we are at the end of a bigger nesting, close all parent tags
            level -= 1
            line = '</' + tagstack.pop() + '>' if tagstack else ''
            tree.append(indentstr(level) + line)
    else:
        while tagstack:
            line = '</' + tagstack.pop() + '>' if tagstack else ''
            level -= 1
            tree.append(indentstr(level) + line)
    return tree


def Tree_from(src):
    """
    takes an input 
    returns a pseudo-ast 
    """
    structured_lines = LineStructureFactory(src)
    if not structured_lines:
        # probably better in LineStructureFactory. E.g.: if there's a list of
        # non LineStructures, to differentiate from a valid LineStructures-List
        raise Exception("Can't parse source of type: %s." % type(src))
    ast = pseudoAST_from(structured_lines)
    tree = html_tree_from_ast(ast)
    return tree


def HTML_from_t5html(src):
    """
    takes a string in t5html format
    returns a string as HTML5
    """
    return '\n'.join(Tree_from(src)).strip()
    

if __name__ == '__main__':
    print("This file is meant to be imported, not to be executed.")


# vi: set et ts=4 ts=4 ai cc=78 rnu so=5 nuw=4:
