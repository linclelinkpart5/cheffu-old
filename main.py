import argparse
import json

from cheffu.tokenize import tokenize
from cheffu.nodify import nodify
from cheffu.graph import generate_graph

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parses recipe files written in Cheffu')
    arg_parser.add_argument('recipe_file_path', metavar='RECIPE FILE PATH', type=str, help='input recipe file path to process')
    arg_parser.add_argument('--output-diagram', metavar='DIAGRAM FILE PATH', type=str, default=None, help='if specified, outputs a diagram of the grammer in PNG format to the specified file path')

    args = arg_parser.parse_args()

    with open(args.recipe_file_path) as recipe_file:
        recipe_text = recipe_file.read()
        tokens = tokenize(recipe_text)
        nodes = nodify(tokens)

        if args.output_diagram:
            graph = generate_graph(nodes)
            graph.write_png(args.output_diagram)