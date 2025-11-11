import pytest
from os import getcwd

from chakram import __version__
from chakram.parser import Parser, Syntax_Error
from chakram.parser import parse_source_program, parse_source_program_as_string
from chakram.parser import get_source_program_symbol_table, get_source_program_symbol_table_as_json
from chakram.parser import get_source_program_as_ast, get_source_program_ast_as_string, get_source_program_ast_as_json
from .fixture.program_1_parse_tree import program_example_1_parse_tree
from .fixture.program_2_parse_tree import program_example_2_parse_tree
from .fixture.program_3_parse_tree import program_example_3_parse_tree
from .fixture.program_1_ast import program_example_1_ast, program_simple_ast_symbols, program_example_1_ast_meta
from .fixture.program_1_ast import program_simple_ast_symbols_as_json, program_example_1_ast_symbols_as_json, program_example_1_ast_symbols, program_simple_ast_symbols
from .fixture.program_1_ast_json import program_examle_1_ast_json_meta

def test_version() -> None:
    assert __version__ == '1.2.10'

def test_program_1_parse_tree(program_example_1_parse_tree: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        parser = Parser(file.read())

        assert(str(parser.get_parse_tree()) == program_example_1_parse_tree)

def test_program_2_parse_tree(program_example_2_parse_tree: str) -> None:
    with open(getcwd() + '/examples/2.b') as file:
        parser = Parser(file.read())
        assert(str(parser.get_parse_tree()) == program_example_2_parse_tree)

def test_parse_source_program(program_example_1_parse_tree: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        assert(str(parse_source_program(file.read())) == program_example_1_parse_tree)

        with open(getcwd() + '/test/fixture/bad.b') as file:
            with pytest.raises(Syntax_Error):
                parse_source_program(file.read())

def test_parse_source_program_as_valid_syntax() -> None:
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

def test_get_source_program_symbol_table(program_simple_ast_symbols_as_json: str) -> None:
    with open(getcwd() + '/examples/simple.b') as file:
        import json
        test_contents = file.read()
        test = json.dumps(get_source_program_symbol_table(test_contents))
        assert(program_simple_ast_symbols_as_json == test)
        with open(getcwd() + '/test/fixture/bad.b') as file:
            test_contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_symbol_table(test_contents)

def test_get_source_program_symbol_table_as_json(program_example_1_ast_symbols_as_json: str) -> None:
        with open(getcwd() + '/test/fixture/bad.b') as file:
            test_contents = file.read()
            with pytest.raises(Syntax_Error):
                get_source_program_symbol_table_as_json(test_contents)

        with open(getcwd() + '/examples/1.b') as file:
            test_contents = file.read()
            assert(program_example_1_ast_symbols_as_json == get_source_program_symbol_table_as_json(test_contents))