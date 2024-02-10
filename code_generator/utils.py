import ast


def pprintast(parsed_ast, indent=1):
    print(ast.dump(parsed_ast, indent=indent))
