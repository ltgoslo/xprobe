import gzip
import sys
import helpers

counter = 0
classes = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}


def f(w):
    return ((w - 1) // 4) - 1


with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        if counter >= 120000:
            # outfile.write(line)
            break

        c_tokens, c_tree = helpers.process(line)
        n_words = len(c_tokens)

        # running this bad boy first so all the length filtering is here
        if n_words < 5 or n_words > 28:
            continue

        if classes[f(n_words)] >= 20000:
            # outfile.write(line)
            continue

        sys.stdout.write("{}\t{}\n".format(" ".join([i['form'] for i in c_tokens]), f(n_words)))
        classes[f(n_words)] += 1
        counter += 1
