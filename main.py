import argparse

from pathlib import Path

from cheffu.tokenize import tokenize
from cheffu.validate import validate
from cheffu.graph import generate_graph

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parses recipe files written in Cheffu')
    arg_parser.add_argument('recipe_file_path', metavar='RECIPE FILE PATH', type=Path, help='input recipe file path to process')
    arg_parser.add_argument('--output-diagram', action='store_true', help='if specified, outputs a diagram of the recipe')
    arg_parser.add_argument('--diagram_file_path', metavar='DIAGRAM FILE PATH', type=Path, default=Path('recipe.png'), help='if output-diagram is specified, outputs the diagram to this specified file path; defaults to the same directory as the recipe file')

    args = arg_parser.parse_args()

    with args.recipe_file_path.open() as recipe_file:
        recipe_text = recipe_file.read()
        tokens = tokenize(recipe_text)
        token_tree = validate(tokens)

        if args.output_diagram:
            graph = generate_graph(token_tree)
            graph.write_png(str(args.diagram_file_path))