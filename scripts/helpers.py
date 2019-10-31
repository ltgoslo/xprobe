import gzip
import conllu


def process(line):
    c_tokens = conllu.parse(line.replace("\\n", "\n"))[0]
    c_tree = c_tokens.to_tree()

    return c_tokens, c_tree
