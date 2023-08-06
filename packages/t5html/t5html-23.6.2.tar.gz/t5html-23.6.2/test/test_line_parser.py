from t5html.lineparser import *

import pytest
from textwrap import dedent
from collections import namedtuple


class TestLineClassifiers:
    def test_classify_comment_line(s):
        assert classify_line('## Some comment') == "comment"

    def test_classify_continue_line(s):
        assert classify_line('.. follow up') == "continue"

    def test_classify_verbatim_line(s):
        assert classify_line('!! <!- html comment -->') == "verbatim"
        
    def test_classify_element_line(s):
        assert classify_line('      div#gallery.blog') == "element"

    def test_classify_import_line(s):
        assert classify_line('@ path/to/file') == "import"


tdata_indent = [ ('', 0), (' '*3, 1), (' '*6, 2), (' '*7, 2), ('\t'*3, 0) ]
@pytest.mark.parametrize("input, expected", tdata_indent)
def test_indent_level(input, expected):
    assert get_indent_level(input) == expected


class TestLineParsing:
    """
    # t5html

    HTML5 := <!DOCTYPE html>
    !! HTML5
    @@ file from src

    html
       head
          title > "t5html example
       body
       header | nav
       main
          article
             section
                "text node
                .. over multiple line
          article
             section
    """
    def setup_class(c):
        c._html = dedent(c.__doc__)

    def test_doc_as_text(s):
        assert '# t5html' in s._html

    def test_indentation(s):
        body = [l for l in s._html.splitlines() if 'body' in l][0]
        title = [l for l in s._html.splitlines() if 'title' in l][0]
        assert 'body' in body and get_indent_level(body) == 1
        assert 'title' in title and get_indent_level(title) == 2

    def test_classify_lines(s):
        b, c, n, m, v, i, cc, t =\
        "blank comment element macro verbatim import continue text".split()
        manual = enumerate([b,c,b,m,v,i,b,*(n,)*8,t,cc,n,n])
        auto = enumerate(map(classify_line, s._html.splitlines()))
        assert list(auto) == list(manual)

    def test_RawLineStructure_fromRawString(s):
        rls = RawLines_from_str(s._html)
        assert rls[1] == (1, '# t5html')
        assert rls[-1] == (18, ' '*9+'section')

    def test_classifed_LineStructure(s):
        cls = LineStructures_from_RawLines(
                RawLines_from_str(s._html))
        assert cls[1] == (1, '# t5html', 'comment')
        assert cls[-1] == (18, ' '*9+'section', 'element')

    def test_sanitized_cls(s):
        scls = sanitized_LineStructures(
                LineStructures_from_RawLines(
                    RawLines_from_str(s._html)))
        assert scls[0] == (3, 'HTML5 := <!DOCTYPE html>', 'macro')
        assert scls[1] == (4, '!! HTML5', 'verbatim')
        assert scls[2] == (5, '@@ file from src', 'import')
        assert scls[-3] == (16, ' '*12+'.. over multiple line', 'continue')
        assert scls[-1] == (18, ' '*9+'section', 'element')

    
class TestSanitizedLineParsing:
    """
    # t5html

    HTML5 := <!DOCTYPE html>
    !! HTML5
    @@ file from src

    html
       head
          title > "t5html example
       body
       header | nav
       main
          article
             section
                "text node
                .. over multiple line
          article
             section
    """
    def setup_class(c):
        c._html = dedent(c.__doc__)
        c._scls = sanitized_LineStructures(
                    LineStructures_from_RawLines(
                        RawLines_from_str(c._html)))

    def test_extract_macros(s):
        macros, cls = split_macros(s._scls)
        assert macros == [(3, 'HTML5 := <!DOCTYPE html>', 'macro')]
        assert (4, '!! HTML5', 'verbatim') in cls
        assert (5, '@@ file from src', 'import') in cls

    def test_extract_imports(s):
        imports, cls = split_imports(s._scls)
        assert imports == [(5, '@@ file from src', 'import')]
        assert (3, 'HTML5 := <!DOCTYPE html>', 'macro') in cls
        assert (4, '!! HTML5', 'verbatim') in cls

    def test_macrodef_from_LineStructure(s):
        macros, cls = split_macros(s._scls)
        assert MacroDef_from_LineStructures(macros) == {'HTML5' : '<!DOCTYPE html>'}

    def test_expand_macro(s):
        macros, cls = split_macros(s._scls)
        macrodef = MacroDef_from_LineStructures(macros)
        assert '!! <!DOCTYPE html>' in [tpl.line for tpl in expand_macros(cls, macrodef)]

    def test_concatenate_lines_lessmocked(s):
        lines = content_from_ls(concatenate_lines(s._scls))
        assert ' '*12+'"text node over multiple line' in lines
        lines = concatenate_lines(s._scls)
        assert (15, ' '*12+'"text node over multiple line', 'text') in lines

    def test_concatenate_lines_mocked(s):
        lines = [LineStructure(0, '"Text Node', 'text'),
                LineStructure(1, '.. over multiple lines.', 'continue')]
        assert '"Text Node over multiple lines.' in concatenate_lines(lines)[0].line
        lines = [LineStructure(0, '"Text Node', 'text'),
                LineStructure(1, '..over multiple lines.', 'continue')]
        assert '"Text Nodeover multiple lines.' in concatenate_lines(lines)[0].line
        lines = [LineStructure(0, '"Text Node', 'text'),
                LineStructure(1, '.. over multiple lines.', 'continue')]
        assert [LineStructure(0, '"Text Node over multiple lines.', 'text'),
                ] == concatenate_lines(lines)

    def test_split_fold(s):
        foldseq = list(">|<")
        line = "p > c | s < p"
        assert split_fold(line, foldseq) == ['p', 'c', 's', 'p']

    def test_line_folding_1(s):
        line = "parent > child "
        assert fold_lines([LineStructure(0, line, 'element')]) == [
                LineStructure(0, 'parent', 'element'),
                LineStructure(0, '   child ', 'element')]

    def test_line_folding_2(s):
        line = "parent | sibling"
        assert fold_lines([LineStructure(0, line, 'element')]) == [
                LineStructure(0, 'parent', 'element'),
                LineStructure(0, 'sibling', 'element')]

    def test_line_folding_3(s):
        line = "parent > child | sibling"
        assert fold_lines([LineStructure(0, line, 'element')]) == [
                LineStructure(0, 'parent', 'element'),
                LineStructure(0, '   child', 'element'),
                LineStructure(0, '   sibling', 'element')]

    def test_line_folding_4(s):
        line = "parent > child | sibling < parent"
        assert fold_lines([LineStructure(0, line, 'element')]) == [
                LineStructure(0, 'parent', 'element'),
                LineStructure(0, '   child', 'element'),
                LineStructure(0, '   sibling', 'element'),
                LineStructure(0, 'parent', 'element')]

    def test_line_folding_5(s):
        "root element is already indented"
        line = "   parent > child | sibling < parent"
        assert fold_lines([LineStructure(0, line, 'element')]) == [
                LineStructure(0, '   parent', 'element'),
                LineStructure(0, '      child', 'element'),
                LineStructure(0, '      sibling', 'element'),
                LineStructure(0, '   parent', 'element')]



# vi: set et ts=4 ts=4 ai cc=78 nowrap nu rnu so=5:
