import pytest

from os import path, listdir
from glob import glob

def test_docs_exist():
    """ make sure we have documentation """ 
    assert path.isdir('doc')

def test_docs_non_empty():
    """doc dir is not empty"""
    assert len(listdir('doc')) > 0

def test_doc_readme_exists():
    """at least 1 readme file"""
    assert len(glob('doc/ReadMe*')) > 0
    

# vi: set et ts=4 ts=4 ai :
