from lark import Lark, Tree
from xion.transformer import AST_Transformer, AST_Node
import os
import json
import logging

# Initialize logging for lark.
logging.basicConfig(level=logging.DEBUG)


class Parser:
    """Parser and adapter with lark.

    Build and transform a parse tree for syntax-directed translation of
    a source program. Initializes with the provided LALR(1) lark grammar.

    Args:
        source_program: The source B program.
        transformer: Syntax-directed transformer.
        debug: Debug flag in Lark.
        grammar: Optional alternative LALR(1) grammar that passes to lark.

    Attributes:
        source_program: The source program.
        transformer: Syntax-directed transformer.
        parser: Lark LALR(1) parser instance.
        grammar: LALR(1) grammar that passes to lark.
        tree: Parse tree.

    """
    def __init__(self, source_program: str, debug=True, grammar=f'{os.path.dirname(__file__)}/grammar.lark') -> None:
        self.source: str = source_program
        self._read_grammar(grammar)
        self.parser = Lark(
            self.grammar,
            start='program',
            parser='lalr',
            debug=True)
        self._tree = self.parser.parse(self.source)

    def __str__(self) -> str:
        """The parse tree as formatted string """
        return self._tree.pretty()

    def get_parse_tree(self) -> Tree:
        """Get the current parse tree.

        Returns:
            The current state of the parse tree.

        """
        return self._tree

    def print_parse_tree(self, pretty=False, file=None) -> None:
        """Print parse tree.

        Print the parse tree to a text stream.

        Args:
            pretty: Print as formatted string
            file: text stream
        """
        if pretty is True:
            print(self._tree.pretty(), file=file)
        else:
            print(self.get_parse_tree(), file=file)

    def _read_grammar(self, location: str) -> None:
        """Read source grammar.

        Read a grammar from location on disk.

        Args:
            grammar: The source LALR(1) grammar.

        """
        with open(location) as file:
            self.grammar = file.read()


def parse_source_program(source_program: str, debug=True) -> Tree:
    """ Get parse tree of B program as serializable tree (Lark.Tree)

    Args:
        source_program: The source B program as a string
        debug: debug flag

    Returns:
        Serializable parse tree

    """
    return Parser(source_program, debug=debug).get_parse_tree()


def parse_source_program_as_string(source_program: str, pretty: bool = True, debug=True) -> str:
    """ Get parse tree of B program as serializable tree (Lark.Tree)

    Args:
        source_program: The source B program as a string
        debug: debug flag

    Returns:
        Parse tree as string

    """
    if pretty:
        return parse_source_program(source_program, debug).pretty()
    else:
        return str(parse_source_program(source_program, debug))


def get_source_program_as_ast(source_program: str, meta=False, debug=True) -> AST_Node:
    """ Get AST of B program (Lark.Tree)

    Args:
        source_program: The source B program as a string
        meta: Enable semantic meta data flag
        debug: debug flag

    Returns:
        Tree[AST]

    """
    tree = Parser(source_program, debug=debug).get_parse_tree()
    ast: AST_Node = AST_Transformer(use_meta=meta).transform(tree)
    return ast


def get_source_program_ast_as_string(source_program: str, meta=False, debug=True) -> str:
    """ Get AST of B program as string

    Args:
        source_program: The source B program as a string
        meta: Enable semantic meta data flag
        debug: debug flag

    Returns:
        AST as string

    """
    tree = Parser(source_program, debug=debug).get_parse_tree()
    ast = AST_Transformer(use_meta=meta).transform(tree)
    return str(ast)


def get_source_program_ast_as_json(source_program: str, meta=False, debug=True):
    """ Get AST of B program as json

    Args:
        source_program: The source B program as a string
        meta: Enable semantic meta data flag
        debug: Debug flag

    Returns:
        AST as json dump

    """
    tree = Parser(source_program, debug=debug).get_parse_tree()
    ast = AST_Transformer(use_meta=meta).transform(tree)
    return json.dumps(ast)
