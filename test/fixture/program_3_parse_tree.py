import pytest


@pytest.fixture  # type: ignore
def program_example_3_parse_tree() -> str:
    return """program
  definition
    function_definition
      snide
      parameters
        rvalue
          lvalue_expression
            identifier    errno
      block_statement
        statement
          extrn_statement
            wr.unit
            mess
            ;
        statement
          auto_statement
            identifier    u
            ;
        statement
          rvalue_statement
            expression
              rvalue
                assignment_expression
                  identifier    u
                  assignment_operator
                    =
                    None
                  rvalue
                    lvalue_expression
                      identifier    wr.unit
              ;
            expression
              rvalue
                assignment_expression
                  identifier    wr.unit
                  assignment_operator
                    =
                    None
                  rvalue
                    constant_expression
                      integer_literal    1
              ;
            expression
              rvalue
                function_expression
                  identifier    printf
                  parameters
                    rvalue
                      constant_expression
                        string_literal    "error number %d, %s*n'*,errno,mess[errno]"
              ;
            expression
              rvalue
                assignment_expression
                  identifier    wr.unit
                  assignment_operator
                    =
                    None
                  rvalue
                    lvalue_expression
                      identifier    u
              ;
  definition
    vector_definition
      mess
      integer_literal    5
      ival
        string_literal    "too bad"
      ival
        string_literal    "tough luck"
      ival
        string_literal    "sorry, Charlie"
      ival
        string_literal    "that's the breaks"
      ival
        string_literal    "what a shame"
      ival
        string_literal    "some days you can't win"
      ;\n"""
