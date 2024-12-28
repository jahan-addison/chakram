from __future__ import annotations
from lark import Transformer, Discard
from typing import TypedDict, Union, List, Optional, TypeVar, Literal, NotRequired

T = TypeVar('T', bound='AST_Node')

Node = Union[List[T], T]
Constant_Type = List[str]
Operator_Type = List[Union[str, None]]
Node_Root = Union[Operator_Type, str, int]
Node_Type = Union[Literal['statement'], Literal['expression'], Operator_Type, str]


class AST_Node(TypedDict):
    """The AST data structure"""
    node: Node_Type
    root: Node_Root
    left: NotRequired[Node]
    right: NotRequired[Node]


Definitions = List[AST_Node]


class AST_Transformer(Transformer):
    """
        AST transformer class.

        Transform a parse tree into an AST for future passes and semantic
        optimizations.

        A B program is structured by definitions - one of either a vector
        or function. Functions contain expressions (rvalues) or statements. These
        are the mutual recursive branches we care about most. Lvalues and lvalue
        expressions are generally flattened, along with constant literals types.
    """

    """ Language operator map. """
    operator_map = {
        'unary_dec': '--',
        'unary_inc': '++',
        'or_operator': '|',
        'and_operator': '&',
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

    def __construct_node(self,
                         type: Node_Type,
                         root: Node_Root,
                         left: Optional[Node] = None,
                         right: Optional[Node] = None) -> AST_Node:
        """ AST Node factory method. """
        node: AST_Node = {
            'node': type,
            'root': root,
        }
        if left is not None:
            node['left'] = left

        if right is not None:
            node['right'] = right

        return node

    """Program. """
    def program(self, args) -> AST_Node:
        return self.__construct_node('program', 'definitions', left=args)

    """ Definitions. """
    def definition(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def ival(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def function_definition(self, args) -> AST_Node:
        return self.__construct_node('function_definition', args[0].value, left=args[1].children, right=args[2])

    def vector_definition(self, args) -> AST_Node:
        return self.__construct_node('vector_definition', args[0].value, left=args[1], right=args[2:])

    """ Mutual-recursive Branches. """
    def rvalue(self, args) -> AST_Node:
        return args[0]

    def statement(self, args) -> AST_Node:
        return args[0]

    def expression(self, args) -> AST_Node:
        return args

    """ Statements. """
    def __construct_statement_node(self, root:
                                   Node_Root,
                                   left: Optional[Node] = None,
                                   right: Optional[Node] = None) -> AST_Node:
        """ Statement AST Node factory method.  """
        return self.__construct_node('statement', root, left=left, right=right)

    def block_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('block', left=args)

    def rvalue_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('rvalue', left=args)

    def switch_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('switch', left=args[0], right=args[1:])

    def case_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('case', left=args[0], right=args[1:])

    def return_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('return', left=args)

    def while_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('while', left=args[0], right=args[1])

    def if_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('if', left=args[0], right=args[1])

    def goto_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('goto', left=self.__to_identifier(args[0]))

    def label_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('label', left=self.__to_identifier(args[0]))

    def extrn_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('extrn', left=list(map(lambda lvalue: self.__to_identifier(lvalue), args)))

    def auto_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('auto', left=args)

    def break_statement(self, args) -> AST_Node:
        return self.__construct_statement_node('break')

    """ Expressions. """

    def function_expression(self, args) -> AST_Node:
        return self.__construct_node('function_expression', args[0]['root'], left=args[0], right=args[1].children)

    def relation_expression(self, args) -> AST_Node:
        return self.__construct_node('relation_expression',
                                     [self.operator_map[args[1].data]],
                                     left=args[0],
                                     right=args[2])

    def ternary_expression(self, args) -> AST_Node:
        return self.__construct_node('ternary_expression', args[0], left=args[1], right=args[2])

    def lvalue_expression(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def constant_expression(self, args) -> AST_Node:
        """ Passthrough"""
        return args[0]

    def unary_expression(self, args) -> AST_Node:
        return self.__construct_node('unary_expression', [self.operator_map[args[0].data.value]], left=args[1])

    def evaluated_expression(self, args) -> AST_Node:
        return self.__construct_node('evaluated_expression', args[0])

    def address_of_expression(self, args) -> AST_Node:
        return self.__construct_node('address_of_expression', ['&'], left=args[1])

    def post_inc_dec_expression(self, args) -> AST_Node:
        return self.__construct_node('post_inc_dec_expression',
                                     [self.operator_map[args[1].data.value]],
                                     right=args[0])

    def pre_inc_dec_expression(self, args) -> AST_Node:
        return self.__construct_node('pre_inc_dec_expression',
                                     [self.operator_map[args[0].data.value]],
                                     left=args[1])

    def assignment_expression(self, args) -> AST_Node:
        return self.__construct_node('assignment_expression', args[1], left=args[0], right=args[2])

    def assignment_operator(self, args) -> Operator_Type:
        return ['=', args[1] if args[1] is None else self.operator_map[args[1].data]]

    """ Inline Lvalue grammar productions. """

    def __to_identifier(self, args) -> AST_Node:
        return self.__construct_node('lvalue', args.value)

    def identifier(self, args) -> AST_Node:
        return self.__construct_node('lvalue', args[0].value)

    def indirect_identifier(self, args) -> AST_Node:
        return self.__construct_node('indirect_lvalue', ['*'], left=args[1])

    def vector_identifier(self, args) -> AST_Node:
        return self.__construct_node('vector_lvalue', args[0]['root'], left=args[1])

    """ Constants. """

    def __construct_constant_node(self, type: Node_Type, root: Node_Root) -> AST_Node:
        """ Constant Literal AST Node factory method.  """
        return self.__construct_node(type, root, left=None, right=None)

    def number_literal(self, args) -> AST_Node:
        return self.__construct_constant_node('number_literal', int(''.join(args)))

    def string_literal(self, args) -> AST_Node:
        return self.__construct_constant_node('string_literal', ''.join(args))

    def constant_literal(self, args) -> AST_Node:
        return self.__construct_constant_node('constant_literal', ''.join(args))

    def SEMI_COLON(self, name):
        """Throw away ';' """
        return Discard
