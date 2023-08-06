""" 
importer

helps to import additional files. 

ATM: only macro-definitions can be imported. The logic behind tree or partial
    tree imports is not resolved.

Examples:
=========

@@ file from path 
@@ file

"""
from os import path, getcwd


IMPLICIT_IMPORT_PATH = '~/.local/share/t5html'
CWD = getcwd()
FILE_LIST = []


def path_from_import_string(s):
    """
    takes an import str (e.g.: @@ fname from path)
    returns a path-str
    """
    rm_head = lambda s: s.lstrip().lstrip('@@').lstrip()
    if not 'from' in s:
        user_local = path.expanduser(IMPLICIT_IMPORT_PATH)
        return path.join(user_local, rm_head(s))
    fname, rest = rm_head(s).split('from', 1)
    fpath = rest.strip()
    return path.join(fpath, fname.strip())


def path_from_LineStructure(ls):
    """
    takes a LineStructure
    returns a path
    """
    if not (ls.cls == "import" and  ls.line.startswith('@@')):
        errortext = f"Not a vaild import at line {ls.nr}: {ls.line}"
        raise Exception(errortext)
    
    return path_from_import_string(ls.line)


def list_of_imports(lst):
    """
    takes a list of linestructures
    returns a list of pathnames
    """
    pfLS = path_from_LineStructure
    paths = [pfLS(ls) for ls in lst if ls.cls == 'import']
    return paths


def existing_imports(lst):
    """
    takes a list of pathnames
    returns a list of existing files
    """
    rootdir = path.dirname(FILE_LIST[0]) if FILE_LIST else ''
    paths = []

    for p in lst:
        if p.startswith('./'):
            expanded_path = path.join(rootdir, p)
        else:
            expanded_path = p
        paths.append(expanded_path)

            
    paths = [path.normpath(p) for p in paths if path.isfile(p)]
    return paths


def readfile(fpath):
    """
    takes a str with a filepath
    returns the raw text/file-content

    additionaly appends it to the FILE_LIST. First item is the root file.
    """
    with open(fpath) as f:
        raw = open(fpath).read()
        FILE_LIST.append(fpath)
        return raw


if __name__ == '__main__':
    print("This file is meant to be imported, not to be executed.")


# vi: set et ts=4 ts=4 ai cc=78 rnu so=5 nuw=4:
