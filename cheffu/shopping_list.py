import cheffu.constants as c

def shopping_list(token_tree_root):
    def recurse(token_tree):
        # Process inputs recursively
        input_results = []
        if 'inputs' in token_tree:
            for i in token_tree['inputs']:
                input_results.extend(recurse(i))

        # Find out what kind of token this is
        sigil = token_tree['sigil']

        # We only care about ingredients
        if sigil == c.OPERAND_SIGIL and 'name' in token_tree:
            return input_results + [token_tree['name']]
        else:
            return input_results

    return set(recurse(token_tree_root))