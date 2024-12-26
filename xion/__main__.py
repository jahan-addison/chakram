
if __name__ == '__main__':
    from xion.parser import get_source_program_ast_as_string, parse_source_program_as_string
    from argparse import ArgumentParser

    args_parser = ArgumentParser()
    args_parser.add_argument("-f", "--file",
                             dest="filename", help="write report to FILE", metavar="FILE")
    args_parser.add_argument("-p", "--pretty", required=False, action='store_true',
                             dest="pretty", default=False, help="pretty print parse tree")
    # for testing
    args_parser.add_argument("-pt", "--pt", required=False, action='store_true',
                             dest="pt", default=False, help="get verbose parse tree")

    args = args_parser.parse_args()

    with open(args.filename) as file:
        if args.pt:
            print(parse_source_program_as_string(file.read(), pretty=args.pretty))
        else:
            print(get_source_program_ast_as_string(file.read(), pretty=args.pretty))
