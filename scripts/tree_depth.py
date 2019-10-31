import sys
import nltk
from helpers import process

def depth(t):
    if not t.children:
        return 1

    return max([1 + depth(i) for i in t.children])

def f(w):
    return ((w - 1) // 4) - 1

sizes = {i: {j: 0 for j in range(3, 8)} for i in range(6)}
combinations = sum(len(i) for i in sizes.values())
maximum = 120000 / combinations

counter = 0
with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        if counter >= 120000:
            break

        try:
            words, tree = process(line)
        except:
            continue

        if len(words) < 5 or len(words) > 28:
            continue
        bucket = f(len(words))
        height = depth(tree)
        
        if height >  7 or height < 3 or sizes[bucket][height] >= maximum:
            # outfile.write(line)
            continue

        sizes[bucket][height] += 1
        counter += 1
        sys.stdout.write("{}\t{}\n".format(" ".join(i['form'] for i in words), height))
