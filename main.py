import argparse
import json

# from parsers.modgrammar_token import generate_graph
from cheffu.tokenize import tokenize
from cheffu.nodify import nodify

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Parses recipe files written in Cheffu')
    arg_parser.add_argument('recipe_file_paths', metavar='RECIPE FILE NAMES', type=str, nargs='+', help='a list of recipe file names to process')

    args = arg_parser.parse_args()

    for recipe_file_path in args.recipe_file_paths:
        with open(recipe_file_path) as recipe_file:
            recipe_text = recipe_file.read()
            tokens = tokenize(recipe_text)
            nodes = nodify(tokens)
            print(tokens)
            print(nodes)