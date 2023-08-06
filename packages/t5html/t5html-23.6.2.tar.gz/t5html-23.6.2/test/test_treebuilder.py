from t5html.treebuilder import *
from t5html.lineparser import *


import pytest

@pytest.mark.parametrize("src, expected",
                            [('', "Can't parse source of type"),
                             (0, "Can't parse source of type"),
                             ([], "Can't parse source of type"),
                           ])
def test_Tree_from_exception_on_wrong_input_type(src, expected):
    with pytest.raises(Exception) as einfo:
        b = Tree_from(src)
    assert str(einfo.value).startswith(expected)

@pytest.mark.parametrize("src, expected",
        [(pseudoAST_from([LineStructure(0, '!! TEST', 'verbatim')]), list),
         (pseudoAST_from([LineStructure(1, '!! TEST', 'verbatim')])[0], TreeElement)])
def test_pseudoAST_exception_on_correct_input(src, expected):
    assert type(src) == expected

def test_pseudoAST_simple_t5html_input():
    data = 'html > head | body > div#main.imp.test > p > "some text'
    tree = pseudoAST_from(LineStructureFactory(data))
    assert TreeElement(3,'p','<p>',0) in tree
    assert TreeElement(1,'body','<body>',0) in tree

def test_html_from_t5html():
    data = 'html > head | body > div#main.imp.test > p > "some text'
    assert '  </body>' in HTML_from_t5html(data) 

def test_src():
    pass

# vi: set et ts=4 ts=4 ai cc=78 :
