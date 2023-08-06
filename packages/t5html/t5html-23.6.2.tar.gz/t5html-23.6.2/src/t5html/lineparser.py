""" 
LineParser

Contains the functions to process t5html files.

Example:

    Start of line symbols:

        ## comment
        !! verbatim line
        @@ import file
        MACRONAME := macro definition / text
        .. line continuation
    
    Inline symbols:

        > indent
        < dedent
        | keep level (sibling element to previous element)
        " text-node

"""
from . import importer as imp


from collections import namedtuple, OrderedDict
import re


## as we progress from raw-text to html, the data structures 
## continually evolve. Every line itself is structured by
## (original line-number, content of the line)
## the next step is to add a classifier to the structure:
## (original line-number, content of the line, classifier)

RawLine = namedtuple('RawLine', 'nr line')
LineStructure = namedtuple('LineStructure', 'nr line cls')


def get_indent_level(line):
    """
    takes a string representing a line 
    returns a number representing the indentation-level
    """
    # Because of the line-continuation symbol beeing two dots followed
    # by a space, the *reasonable* indentation seems to be 3.
    # explicit only element whitespaces! no tabs, etc.
    count = len(line) - len(line.lstrip(' '))
    # TODO: we don't handle indentation errors, atm!
    level = int(count / 3)
    return level


def RawLines_from_str(text):
    """
    takes a string 
    returns a RawLineStructure [(nr, line), ...]
    """
    rls = [RawLine(n, l.rstrip())
            for n, l in enumerate(text.splitlines())]
    return rls

def RawLines_from_file(fpath):
    """
    takes a file-path as a string
    returns a RawLinesStructure
    """
    text = imp.readfile(fpath)
    return RawLines_from_str(text)


def LineStructures_from_RawLines(rls):
    """
    tales a RawLinesStructure 
    returns a LineStructuresStructure
    """
    cls = [LineStructure(n, l, classify_line(l))
            for n, l in rls]
    return cls


def sanitized_LineStructures(cls):
    """
    takes a LineStructureStructure
    returns a CLS without blanks and comments
    """
    sls = [t for t in cls if t.cls not in ('comment', 'blank')]
    return sls


def split_by_classifier(cls, clsname):
    """
    takes a LineStructuresStructure 
    returns a split by named classifier
    """
    extracted = [t for t in cls if t.cls == clsname] or []
    rest = [t for t in cls if not t.cls == clsname]
    return extracted, rest


def split_macros(scls):
    """
    takes a LineStructuresStructure
    returns two lists: (macros, scls without macros)
    """
    return split_by_classifier(scls, 'macro')
    

def split_imports(scls):
    """
    takes a LineStructuresStructure
    returns two lists: (imports, scls without imports)
    """
    return split_by_classifier(scls, 'import')
    

def classify_line(line):
    """
    takes a str representing a line
    returns a string classifying the type of line

    atm, there are 8 line-cllassifiers:
        blank, comment, continue, element, import, macro, text, verbatim
    """
    l = line.strip()
    # single classifier allowed:
    if l == '': return 'blank'

    if l.startswith('#'): return "comment"
    if l.startswith('!'): return "verbatim"
    if l.startswith('@'): return "import"
    if l.startswith('"'): return "text"

    # has to be a double-classifier
    if l.startswith('..'): return "continue"
    if ' := ' in l and l.split(' := ', 1)[0].isupper():
        return 'macro'

    return "element"


def MacroDef_from_LineStructures(cls):
    """
    takes classifiedLines
    returns a OrderedDict of MacorKey: MacroValue
    """
    macrodef = OrderedDict()
    for m in cls:
        k, v = m.line.split(' := ')
        macrodef[k] = v
    return macrodef
    

def Imports_from_LineStructures(cls):
    """
    takes classifiedLines
    returns a OrderedDict of MacorKey: MacroValue
    """
    imports = OrderedDict()
    for i in cls:
        k, v = i.line.lstrip('@ ')
        imports[k] = v
    return imports


def expand_macros(cls, macros, visited={}):
    """
    takes LineStructures
    returns LineStructures, but without macros.

    """
    # This function is somewhat messy.
    # we hold the visited-dictionary to prevent recursive macro-expansion.
    # basically we go over every line and check every macro if its in the
    # line and the macro hasnt already be expanded in that line.
    #
    macro_free = []
    for ls in cls:          # ls = line structure (nr, line, cls)
        line = ls.line
        for m in macros:
            if m in line:
                lines_visited = visited.get(m, [])
                if not lines_visited or not ls.nr in lines_visited:
                    line = ls.line.replace(m, macros[m])
                    lines_visited.append(ls.nr)
                    if m in line:
                        visited[m] = lines_visited
            
                
        macro_free.append(LineStructure(ls.nr, line, ls.cls))
        
    return macro_free if macro_free else cls


def concatenate_lines(ls):
    """
    takes a list of LineStructures and 
    returns a list of concatenated LineStructures, without 'continue' lines
    """
    concatenated = []
    for current in ls:
        new = current
        if current.cls == 'continue':
            lastline = concatenated.pop()
            new_content = lastline.line + current.line.lstrip().lstrip('.')
            new = LineStructure(lastline.nr,
                                new_content,
                                lastline.cls)
        concatenated.append(new)

    return concatenated

FOLDS = re.compile(r' (<|>|\|) ')
def fold_lines(ls):
    """
    takes a list of  LineStructures
    returns a list of LineStructures
    """
    folded = []
    for current in ls:
        foldseq = FOLDS.findall(current.line)
        if not foldseq:
            folded.append(current)
            continue

        lines = split_fold(current.line, foldseq)
        level = get_indent_level(lines[0])
        for idx, fold in enumerate(foldseq, start=1):
            level = level + 1 if fold == '>' else level
            level = level - 1 if fold == '<' else level
            level = level if level > 0 else 0
            indent = (3 * level) * ' '
            lines[idx] = indent + lines[idx]

        for line in lines:
            folded.append(LineStructure(current.nr, line, current.cls))
    return folded


def split_fold(linestr, foldseq):
    """
    takes a line as string and a sequence of fold-symbols to
    return a list of lines splitted by the fold-symbols
    """
    folded, line = [], linestr
    for sym in foldseq:
        line, nextline = line.split(sym, 1)
        folded.append(line.rstrip())
        line = nextline.lstrip()
    else:
        folded.append(line.lstrip())
    return folded


def import_files(imports):
    """
    takes a list of pathnames
    returns a list of structured lines
    """
    files = imp.existing_imports(imp.list_of_imports(imports))

    all_lines = []
    for f in files:
        raw = RawLines_from_file(f)
        lines = [l for l in normalize_input(raw) if l.cls == 'macro']
        all_lines += lines
    return all_lines



def normalize_input(raw):
    """
    takes a raw t5html fromatted text as a string
    returns a list of Linestructures
    """
    lines = LineStructures_from_RawLines(raw)
    lines = sanitized_LineStructures(lines)
    lines = concatenate_lines(lines)
    return lines


def parse_str(t5html):
    """
    takes a raw string formatted as t5html-text
    returns a completly processed list of LineStrucrues ready to be converted
        to html
    """
    raw = RawLines_from_str(t5html)
    lines = normalize_input(raw)

    macros, lines = split_macros(lines)
    imports, lines = split_imports(lines)

    ilines = import_files(imports)
    macrodef = MacroDef_from_LineStructures(ilines + macros)

    lines = expand_macros(lines, macrodef)
    lines = fold_lines(lines)
    # ISSUE: 2nd expansion needed because of a folding/macro issue
    # the problem stems from the fact we allow macros to contain folding and
    # concatenate symbols: "| < > ..". We would need to clear them before
    # we allow macro-expansion, but then we couldnt have multiline-macros!
    lines = expand_macros(lines, macrodef)

    # reclassify the lines after all the folding and unfolding:
    lines = [LineStructure(l.nr, l.line, classify_line(l.line)) for l in lines]
    return lines


def content_from_ls(ls):
    return [l.line for l in ls]
    

if __name__ == '__main__':
    print("This file is meant to be imported, not to be executed.")


# vi: set et ts=4 ts=4 ai cc=78 rnu so=5 nuw=4:
