from __future__ import annotations
from lark import Transformer, Discard, Tree, Token
from typing import TypedDict, Union, List, Optional, TypeVar, Literal, NotRequired, Dict

T = TypeVar('T', bound='AST_Node')

Node = Union[List[T], T]
Constant_Type = List[str]
Operator_Type = List[Union[str, None]]
Node_Root = Union[Operator_Type, str, int]
Node_Type = Union[Literal['statement'], Literal['expression'], Operator_Type, str]


class _Meta(TypedDict):
    line: Union[int, None]
    type: NotRequired[str]
    size: NotRequired[int]
    column: Union[int, None]
    start_pos: Union[int, None]
    end_pos: Union[int, None]
    end_column: Union[int, None]


class AST_Node(TypedDict):
    """The AST data structure"""
    node: Node_Type
    root: Node_Root
    left: NotRequired[Node]
    right: NotRequired[Node]
    _meta: NotRequired[_Meta]


Symbol_Table = Dict[str, _Meta]

Definitions = List[AST_Node]


class AST_Transformer(Transformer):
    """
        AST transformer and visitor class.

        Transform a parse tree into an AST for future passes and semantic analysis.

        A B program is structured by definitions - one of either a vector
        or function. Functions contain expressions (rvalues) or statements. These
        are the mutual recursive branches we care about most. Lvalues and lvalue
        expressions are generally flattened, along with constant literals types.
    """
    def __init__(self, use_meta=False):
        self._use_meta = use_meta
        self._symbol_table = {}
        super().__init__()

    """ Optionally construct meta table during recursive descent. """
    _use_meta: bool

    """ Constructed global symbol table of lvalues. """

    _symbol_table: Symbol_Table

    """ Language operator map. """
    operator_map = {
        'unary_dec': '--',
        'unary_inc': '++',
        'or_operator': '||',
        'and_operator': '&&',
        'bit_or_operator': '|',
        'bit_and_operator': '&',
        'eq_operator': '==',
        'neq_oeprator': '!=',
        'lt_operator': '<',
        'lte_operator': '<=',
        'gt_operator': '>',
        'gte_operator': '>=',
        'xor_operator': '^',
        'lshift_operator': '<<',
        'rshift_operator': '>>',
        'sub_operator': '-',
        'add_operator': '+',
        'mod_operator': '%',
        'mul_operator': '*',
        'div_operator': '/',
        'unary_indirection': '*',
        'unary_address_of': '&',
        'unary_minus': '-',
        'unary_not': '!',
        'unary_ones_complement': '~'
    }

    def get_symbol_table(self) -> Symbol_Table:
        return self._symbol_table

    def __construct_node(self,
                         token: Union[List[Tree], List[Token], AST_Node],
                         type: Node_Type,
                         root: Node_Root,
                         left: Optional[Node] = None,
                         right: Optional[Node] = None) -> AST_Node:
        """ AST Node factory method. """
        node: AST_Node = {
            'node': type,
            'root': root,
        }

        if self._use_meta is True and isinstance(token, list):
            for item in token:
                if isinstance(item, Tree) or isinstance(item, Token):
                    if isinstance(item, Tree) and not item.meta.empty:
                        node['_meta'] = {
                            'line': item.meta.line,
                            'start_pos': item.meta.start_pos,
                            'column': item.meta.column,
                            'end_pos': item.meta.end_pos,
                            'end_column': item.meta.end_column
                        }
                    elif isinstance(item, Token):
                        node['_meta'] = {
                            'line': item.line,
                            'start_pos': item.start_pos,
                            'column': item.column,
                            'end_pos': item.end_pos,
                            'end_column': item.end_column
                        }

        if left is not None:
            node['left'] = left

        if right is not None:
            node['right'] = right

        return node

    """Program Root. """
    def program(self, args) -> AST_Node:
        return self.__construct_node(args, 'program', 'definitions', left=args)

    """ Definitions. """
    def definition(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def v_size(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def v_symbol(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def function_definition(self, args) -> AST_Node:
        if isinstance(args[0], Token):
            self._symbol_table[str(args[0].value)] = {
                'type': 'function_definition',
                'line': args[0].line,
                'start_pos': args[0].start_pos,
                'column': args[0].column,
                'end_pos': args[0].end_pos,
                'end_column': args[0].end_column
            }
        return self.__construct_node(args, 'function_definition', args[0].value, left=args[1].children, right=args[2])

    def vector_definition(self, args) -> AST_Node:
        if isinstance(args[0], Token):
            self._symbol_table[str(args[0].value)] = {
                'type': 'vector_definition',
                'line': args[0].line,
                'start_pos': args[0].start_pos,
                'column': args[0].column,
                'end_pos': args[0].end_pos,
                'end_column': args[0].end_column
            }
            if (args[1] is not None):
                self._symbol_table[str(args[0].value)]['size'] = int(args[1]["root"])

        return self.__construct_node(args, 'vector_definition', args[0].value, left=args[1], right=args[2:])

    """ Mutual-recursive Branches. """
    def rvalue(self, args) -> AST_Node:
        return args[0]

    def statement(self, args) -> AST_Node:
        return args[0]

    def expression(self, args) -> AST_Node:
        return args

    """ Statements. """
    def __construct_statement_node(self,
                                   token: Union[List[Tree], List[Token], AST_Node],
                                   root: Node_Root,
                                   left: Optional[Node] = None,
                                   right: Optional[Node] = None) -> AST_Node:
        """ Statement AST Node factory method.  """
        return self.__construct_node(token, 'statement', root, left=left, right=right)

    def block_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'block', left=args)

    def rvalue_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'rvalue', left=args)

    def switch_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'switch', left=args[0], right=args[1:])

    def case_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'case', left=args[0], right=args[1:])

    def return_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'return', left=args)

    def while_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'while', left=args[0], right=args[1:])

    def if_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'if', left=args[0], right=args[1:])

    def goto_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'goto', left=[args[0]])

    def label_statement(self, args) -> AST_Node:
        if isinstance(args[0], Token):
            self._symbol_table[args[0].value[:-1]] = {
                'type': 'label',
                'line': args[0].line,
                'start_pos': args[0].start_pos,
                'column': args[0].column,
                'end_pos': args[0].end_pos,
                'end_column': args[0].end_column
            }
        return self.__construct_statement_node(args, 'label', left=[args[0][:-1]])

    def extrn_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'extrn', left=list(map(lambda lvalue: self.__to_identifier(lvalue), args)))

    def auto_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'auto', left=args)

    def break_statement(self, args) -> AST_Node:
        return self.__construct_statement_node(args, 'break')

    """ Expressions. """

    def function_expression(self, args) -> AST_Node:
        return self.__construct_node(args, 'function_expression', args[0]['root'], left=args[0], right=args[1].children)

    def relation_expression(self, args) -> AST_Node:
        return self.__construct_node(args,
                                     'relation_expression',
                                     [self.operator_map[args[1].data]],
                                     left=args[0],
                                     right=args[2])

    def ternary_expression(self, args) -> AST_Node:
        return self.__construct_node(args, 'ternary_expression', args[0], left=args[1], right=args[2])

    def lvalue_expression(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def constant_expression(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def unary_expression(self, args) -> AST_Node:
        return self.__construct_node(args, 'unary_expression', [self.operator_map[args[0].data.value]], left=args[1])

    def unary_operand(self, args) -> AST_Node:
        return args[0]

    def evaluated_expression(self, args) -> AST_Node:
        return self.__construct_node(args, 'evaluated_expression', args[0])

    def address_of_expression(self, args) -> AST_Node:
        return self.__construct_node(args, 'address_of_expression', ['&'], left=args[1])

    def post_inc_dec_expression(self, args) -> AST_Node:
        return self.__construct_node(args,
                                     'post_inc_dec_expression',
                                     [self.operator_map[args[1].data.value]],
                                     right=args[0])

    def pre_inc_dec_expression(self, args) -> AST_Node:
        return self.__construct_node(args,
                                     'pre_inc_dec_expression',
                                     [self.operator_map[args[0].data.value]],
                                     left=args[1])

    def assignment_expression(self, args) -> AST_Node:
        return self.__construct_node(args, 'assignment_expression', args[1], left=args[0], right=args[2])

    def assignment_operator(self, args) -> Operator_Type:
        return ['=']

    """ Inline Lvalue grammar productions. """

    def __to_identifier(self, args) -> AST_Node:
        return self.__construct_node(args, 'lvalue', args.value)

    def identifier(self, args) -> AST_Node:
        node = self.__construct_node(args, 'lvalue', args[0].value)
        if not args[0].value in self._symbol_table:
            self._symbol_table[args[0].value] = {
                'type': 'lvalue',
                'line': args[0].line,
                'start_pos': args[0].start_pos,
                'column': args[0].column,
                'end_pos': args[0].end_pos,
                'end_column': args[0].end_column
            }
        return node

    def indirect_identifier(self, args) -> AST_Node:
        node = self.__construct_node(args, 'indirect_lvalue', ['*'], left=args[1])
        if args[1]['root'] in self._symbol_table:
            self._symbol_table[args[1]['root']]['type'] = 'indirect_lvalue'
        return node

        return node

    def vector_identifier(self, args) -> AST_Node:
        node = self.__construct_node(args, 'vector_lvalue', args[0]['root'], left=args[1])
        if args[0]['root'] in self._symbol_table:
            self._symbol_table[args[0]['root']]['type'] = 'vector_lvalue'
        return node
    """ Constants. """

    def __construct_constant_node(self,
                                  token: Union[List[Tree], List[Token], AST_Node],
                                  type: Node_Type,
                                  root: Node_Root) -> AST_Node:
        """ Constant Literal AST Node factory method.  """
        return self.__construct_node(token, type, root, left=None, right=None)

    def number_literal(self, args) -> AST_Node:
        return self.__construct_constant_node(args, 'number_literal', int(''.join(args)))

    def string_literal(self, args) -> AST_Node:
        return self.__construct_constant_node(args, 'string_literal', ''.join(args))

    def constant_literal(self, args) -> AST_Node:
        return self.__construct_constant_node(args, 'constant_literal', ''.join(args))

    def SEMI_COLON(self, name):
        """Throw away ';' """
        return Discard
