if __name__ == "__main__":
    from chakram import parser
    from argparse import ArgumentParser

    args_parser = ArgumentParser()
    args_parser.add_argument(
        "-f", "--file", dest="filename", help="read from FILE", metavar="FILE"
    )
    args_parser.add_argument(
        "-p",
        "--pretty",
        required=False,
        action="store_true",
        dest="pretty",
        default=False,
        help="pretty print parse tree",
    )
    args_parser.add_argument(
        "-s",
        "--symbols",
        required=False,
        dest="symbols",
        default=False,
        action="store_true",
    )
    args_parser.add_argument(
        "-j", "--json", required=False, dest="json", default=False, action="store_true"
    )
    args_parser.add_argument(
        "-m", "--meta", required=False, dest="meta", default=False, action="store_true"
    )
    # for testing
    args_parser.add_argument(
        "-pt",
        "--pt",
        required=False,
        action="store_true",
        dest="pt",
        default=False,
        help="get verbose parse tree",
    )

    args = args_parser.parse_args()

    with open(args.filename) as file:
        if args.symbols:
            print("Symbols:")
            if args.json:
                print(parser.get_source_program_symbol_table_as_json(file.read()))
                exit(0)
            else:
                print(parser.get_source_program_symbol_table(file.read()))
                exit(0)
        if args.pt:
            print(
                parser.parse_source_program_as_string(file.read(), pretty=args.pretty)
            )
            exit(0)
        elif args.json:
            print(parser.get_source_program_ast_as_json(file.read(), meta=args.meta))
            exit(0)
        else:
            print(parser.get_source_program_ast_as_string(file.read(), meta=args.meta))
