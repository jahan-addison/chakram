import pytest
from os import getcwd

from xion import __version__
from xion.parser import Parser
from xion.parser import parse_source_program, parse_source_program_as_string
from xion.parser import get_source_program_as_ast, get_source_program_ast_as_string, get_source_program_ast_as_json
from .fixture.program_1_parse_tree import program_example_1_parse_tree
from .fixture.program_2_parse_tree import program_example_2_parse_tree
from .fixture.program_3_parse_tree import program_example_3_parse_tree
from .fixture.program_1_ast import program_example_1_ast, program_example_1_ast_meta
from .fixture.program_1_ast_json import program_examle_1_ast_json_meta

def test_version() -> None:
    assert __version__ == '1.1.1'

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

def test_parse_source_program_as_string(program_example_3_parse_tree: str) -> None:
    with open(getcwd() + '/examples/3.b') as file:
        parse_tree = parse_source_program_as_string(file.read())
        assert(parse_tree.replace('\t', ' ' * 4) == program_example_3_parse_tree)

def test_get_source_program_as_ast(program_example_1_ast: str, program_example_1_ast_meta: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        contents = file.read()
        assert(str(get_source_program_as_ast(contents)) == program_example_1_ast)
        assert(str(get_source_program_as_ast(contents, meta=True)) == program_example_1_ast_meta)

def test_get_source_program_ast_as_string(program_example_1_ast: str) -> None:
    with open(getcwd() + '/examples/1.b') as file:
        assert(get_source_program_ast_as_string(file.read()) == program_example_1_ast)

def test_get_source_program_ast_as_json() -> None:
    import json
    with open(getcwd() + '/examples/1.b') as file:
        test_contents = file.read()
        test = json.dumps(get_source_program_as_ast(test_contents))
        assert(test == get_source_program_ast_as_json(test_contents))
