import pytest
from os import getcwd

from xion import __version__
from xion.parser import Parser, Syntax_Error
from xion.parser import parse_source_program, parse_source_program_as_string
from xion.parser import get_source_program_symbol_table, get_source_program_symbol_table_as_json
from xion.parser import get_source_program_as_ast, get_source_program_ast_as_string, get_source_program_ast_as_json
from .fixture.program_1_parse_tree import program_example_1_parse_tree
from .fixture.program_2_parse_tree import program_example_2_parse_tree
from .fixture.program_3_parse_tree import program_example_3_parse_tree
from .fixture.program_1_ast import program_example_1_ast, program_example_1_ast_meta
from .fixture.program_1_ast_json import program_examle_1_ast_json_meta

def test_version() -> None:
    assert __version__ == '1.1.8'

def test_program_1_parse_tree(program_example_1_parse_tree: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        parser = Parser(file.read())

        assert(str(parser.get_parse_tree()) == program_example_1_parse_tree)

def test_program_2_parse_tree(program_example_2_parse_tree: str) -> None:
    with open(getcwd() + '/examples/2.b') as file:
        parser = Parser(file.read())
        assert(str(parser.get_parse_tree()) == program_example_2_parse_tree)

def test_program_3_parse_tree(program_example_3_parse_tree: str) -> None:
    with open(getcwd() + '/examples/3.b') as file:
        parser = Parser(file.read())

        assert(str(parser).replace('\t', ' ' * 4) == program_example_3_parse_tree)

def test_parse_source_program(program_example_1_parse_tree: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        assert(str(parse_source_program(file.read())) == program_example_1_parse_tree)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            with pytest.raises(Syntax_Error):
                parse_source_program(file.read())

def test_parse_source_program_as_string(program_example_3_parse_tree: str) -> None:
    with open(getcwd() + '/examples/3.b') as file:
        parse_tree = parse_source_program_as_string(file.read())
        assert(parse_tree.replace('\t', ' ' * 4) == program_example_3_parse_tree)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            with pytest.raises(Syntax_Error):
                parse_source_program_as_string(file.read())


def test_get_source_program_as_ast(program_example_1_ast: str, program_example_1_ast_meta: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        contents = file.read()
        assert(str(get_source_program_as_ast(contents)) == program_example_1_ast)
        assert(str(get_source_program_as_ast(contents, meta=True)) == program_example_1_ast_meta)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_as_ast(contents)

def test_get_source_program_ast_as_string(program_example_1_ast: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        assert(get_source_program_ast_as_string(file.read()) == program_example_1_ast)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            test_contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_ast_as_string(test_contents)

def test_get_source_program_ast_as_json() -> None:
    import json
    with open(getcwd() + '/examples/1.b') as file:
        test_contents = file.read()
        test = json.dumps(get_source_program_as_ast(test_contents))
        assert(test == get_source_program_ast_as_json(test_contents))

        with open(getcwd() + '/test/fixture/bad.b') as file:
            test_contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_ast_as_json(test_contents)

def test_get_source_program_symbol_table() -> None:
    with open(getcwd() + '/examples/simple.b') as file:
        test_contents = file.read()
        test = {'j': {'type': 'lvalue', 'line': 2, 'start_pos': 18, 'column': 9, 'end_pos': 19, 'end_column': 10}, 'putchar': {'type': 'lvalue', 'line': 5, 'start_pos': 60, 'column': 9, 'end_pos': 67, 'end_column': 16}, 'main': {'type': 'function_definition', 'line': 1, 'start_pos': 0, 'column': 1, 'end_pos': 4, 'end_column': 5}, 'mess': {'type': 'vector_definition', 'line': 10, 'start_pos': 95, 'column': 1, 'end_pos': 99, 'end_column': 5}}
        symbols = get_source_program_symbol_table(test_contents)
        assert(symbols == test)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            test_contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_symbol_table(test_contents)

def test_get_source_program_symbol_table_as_json() -> None:
    with open(getcwd() + '/examples/simple.b') as file:
        test_contents = file.read()
        test = """{"j": {"type": "lvalue", "line": 2, "start_pos": 18, "column": 9, "end_pos": 19, "end_column": 10}, "putchar": {"type": "lvalue", "line": 5, "start_pos": 60, "column": 9, "end_pos": 67, "end_column": 16}, "main": {"type": "function_definition", "line": 1, "start_pos": 0, "column": 1, "end_pos": 4, "end_column": 5}, "mess": {"type": "vector_definition", "line": 10, "start_pos": 95, "column": 1, "end_pos": 99, "end_column": 5}}"""
        symbols = get_source_program_symbol_table_as_json(test_contents)
        assert(symbols == test)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            test_contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_symbol_table_as_json(test_contents)
