import pytest

from t5html.elementparser import *


class Test_Element_Attr_Separation:
    """ 
    Split Elements/Tags with their id and class attributes from the other
    more specific attributes.
    """
    f = staticmethod(separate_element_from_attributes)
    def test_element(s):
        assert s.f('ele') == ('ele', '')

    def test_element_id(s):
        assert s.f('ele#id') == ('ele#id', '')

    def test_element_id_cls(s):
        assert s.f('ele#id.cls') == ('ele#id.cls', '')

    def test_element_cls(s):
        assert s.f('ele.cls') == ('ele.cls', '')

    def test_element_id_2cls(s):
        assert s.f('ele#id.cls.cls') == ('ele#id.cls.cls', '')

    def test_element_2cls(s):
        assert s.f('ele.cls.cls') == ('ele.cls.cls', '')


class Test_Element_Id_Class_Separation:
    """
    Check if there are besides the tag additional id and class attributes.
    """
    f = staticmethod(elementStructure_fromString)
    def test_element(s):
        assert s.f('ele') == ('ele', '', [])

    def test_element_id(s):
        assert s.f('ele#id') == ('ele', 'id', [])

    def test_element_id_cls(s):
        assert s.f('ele#id.cls') == ('ele', 'id', ['cls'])

    def test_element_cls(s):
        assert s.f('ele.cls') == ('ele', '', ['cls'])

    def test_element_id_2cls(s):
        assert s.f('ele#id.cls.cls') == ('ele', 'id', ['cls', 'cls'])

    def test_element_2cls(s):
        assert s.f('ele.cls.cls') == ('ele', '', ['cls', 'cls'])


class Test_Attribute_Conversion:
    """
    Check for normal attribute-str to list conversion.
    """
    f = staticmethod(attributesStructure_fromString)
    def test_attr(s):
        assert s.f('attr') == [(None, 'attr')]
    
    def test_attr_val(s):
        assert s.f('attr=val') == [('attr', 'val')]
    
    def test_2attr(s):
        assert s.f('attr attr') == [(None, 'attr'), (None, 'attr')]

    def test_attr_val_attr(s):
        assert s.f('attr=val attr') == [('attr','val'), (None, 'attr')]

    def test_attr_val_x2(s):
        assert s.f('attr=val attr=val') == [('attr', 'val'), ('attr', 'val')]

    def test_attr_val_2x_quoted(s):
        assert s.f('attr="val" attr=val') == [('attr','val'), ('attr', 'val')]

    def test_attr_namespace(s):
        assert s.f('p:attr') == [(None, 'p:attr')]
    
    def test_attr_ns_val(s):
        assert s.f('p:attr=val') == [('p:attr', 'val')]
    
    def test_attr_text_assignment(s):
        assert s.f('attr="Some text"') == [('attr','Some text')]


class Test_String_From_Attribute_Tuples:
    """
    Check for normal attribute-str to list conversion.
    """
    f = staticmethod(stringify_AttributeStructure)
    def test_string_from_attribute_tuples(s):
        assert s.f([('attr', 'Some text')]) == 'attr="Some text"'

    def test_string_from_attribute_tuples_boolattr(s):
        assert s.f([(None, 'attr')]) == 'attr'

    def test_string_from_attribute_tuples_2boolattr(s):
        assert s.f([(None, 'attr'), (None, 'attr')]) == 'attr attr'

    def test_string_from_attribute_tuples_complex(s):
        _in = [("key", "value"), ("k", 'longer text'), (None, 'attr')]
        _out = 'key="value" k="longer text" attr'
        assert s.f(_in) == _out


class TestComplexAttributeExtraction:
    """
    check for both attribute and tag extraction
    """
    def test_long_element(s):
        _in = 'tag#id.cls.dls.els attr attr=ab attr="abc def" attr=last'
        _out = 'attr attr="ab" attr="abc def" attr="last"'
        ele, attrs = separate_element_from_attributes(_in)
        tpls = attributesStructure_fromString(attrs)
        assert stringify_AttributeStructure(tpls) == _out
        _out = ('tag', 'id', ['cls', 'dls', 'els'])
        assert elementStructure_fromString(ele) == _out


class TestStringifyElementTuple:
    """
    tag head to string
    """
    f = staticmethod(elementStructure_fromString)
    def test_long_element(s):
        _in = s.f('tag#id.cls.dls.els')
        _out = 'tag id="id" class="cls dls els"'
        assert stringify_ElementStructure(_in) == _out


class TestReformatElementLine:
    def test_parse_element(s):
        _in = 'div#myid.cls.cls attr1=value'
        _out = '<div id="myid" class="cls cls" attr1="value">'
        assert parse_element(_in) == _out

    def test_get_tag(s):
        _in = 'div#myid.cls.cls attr1=value'
        _out = '<div id="myid" class="cls cls" attr1="value">'
        assert element_name(parse_element(_in)) == 'div'


# vi: set et ts=4 ts=4 ai cc=78 nowrap nu so=5:
