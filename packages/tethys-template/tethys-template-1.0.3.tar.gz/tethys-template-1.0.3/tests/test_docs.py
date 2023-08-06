import pytest
from tethys import docs


def test_function_with_types_in_docstring():
    assert docs.function_with_types_in_docstring(1, 'two') is True


def test_function_with_pep484_type_annotations():
    assert docs.function_with_pep484_type_annotations(1, 'two') is True


def test_module_level_function_pass():
    assert docs.module_level_function(1, 2) is True


def test_module_level_function_fail():
    with pytest.raises(ValueError):
        docs.module_level_function(1, 1)


def test_example_generator():
    assert list(docs.example_generator(4)) == [0, 1, 2, 3]


def test_example_error():
    with pytest.raises(docs.ExampleError):
        raise docs.ExampleError('Internal Server Error', 500)


def test_example_class():
    c = docs.ExampleClass('test', 200, ['hello', 'world'])
    c.readwrite_property = 'foo'
    assert c.readonly_property == 'readonly_property'
    assert c.readwrite_property == 'foo'
    assert c.example_method(1, 2) is True
    assert c.__special__() is None
    assert c.__special_without_docstring__() is None
    assert c._private() is None
    assert c._private_without_docstring() is None
