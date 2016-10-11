import argparse

from pathlib import Path

from cheffu.tokenize import tokenize
from cheffu.validate import validate
from cheffu.graph import generate_graph
from cheffu.shopping_list import shopping_list
from cheffu.format import format_standard

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parses recipe files written in Cheffu')
    arg_parser.add_argument('recipe_file_path',
                            metavar='RECIPE FILE PATH',
                            type=Path,
                            help='input recipe file path to process',
                            )
    arg_parser.add_argument('--output-diagram',
                            action='store_true',
                            help='if specified, outputs a diagram of the recipe',
                            )
    arg_parser.add_argument('--diagram-file-path',
                            metavar='DIAGRAM FILE PATH',
                            type=Path,
                            default=Path('./recipe.png'),
                            help='if output-diagram is specified, outputs the diagram to this specified file path; defaults to "./recipe.png"',
                            )

    args = arg_parser.parse_args()

    with args.recipe_file_path.open() as recipe_file:
        recipe_text = recipe_file.read()
        tokens = tokenize(recipe_text)
        token_tree = validate(tokens)

        if args.output_diagram:
            graph = generate_graph(token_tree)
            graph.write_png(str(args.diagram_file_path))

        print(sorted(format_standard(token_tree), key=lambda x: x[0]))