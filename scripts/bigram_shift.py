import gzip
import string
import random
import sys
from argparse import ArgumentParser
from nltk.tree import Tree
import helpers

counter = 0
classes = {'I': 0, 'O': 0}

with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        if counter >= 120000:
            # outfile.write(line)
            break

        c_tokens, c_tree = helpers.process(line)
        token_forms = [i['form'] for i in c_tokens]
        if len(token_forms) < 5 or len(token_forms) > 28:
            continue

        # exclude if quotes in sentence
        if '"' in token_forms or '«' in token_forms:
            # outfile.write(line)
            continue


        if random.randint(0, 1):
            if classes['I'] > 60000:
                # outfile.write(line)
                continue

            i = random.randint(0, len(token_forms) - 2)
            if token_forms[i] in string.punctuation or token_forms[i+1] in string.punctuation:
                # outfile.write(line)
                continue

            token_forms[i], token_forms[i + 1] = token_forms[i + 1], token_forms[i]
            classes['I'] += 1
            sys.stdout.write("{}\t{}\n".format(" ".join(token_forms), "I"))

        else:
            if classes['O'] > 60000:
                continue
                # outfile.write(line)

            sys.stdout.write("{}\t{}\n".format(" ".join(token_forms), "O"))

        counter += 1
