import gzip
import pickle
import helpers
import nltk
import sys
import random
import math

subs = {"train": [], "val": []}
nums = {'orig': 0, 'inv': 0}
status = None

# load freqdist
with open(sys.argv[3], "rb") as ser:
    freq_dist = pickle.load(ser)

bigrams = {"NOUN": [], "VERB": []}
counter = 0

with open(sys.argv[1], "r", errors="ignore") as f:
    for line in f:
        c_tokens, c_tree = helpers.process(line)
        words = [(word["form"], word["upostag"]) for word in c_tokens]

        for n, (word, tag) in enumerate(words[1:-1]):
            if tag in ['NOUN', 'VERB']:
                bigrams[tag].append((words[n], words[n + 1]))
                bigrams[tag].append((words[n + 1], words[n + 2]))
                counter += 1

        if counter >= 300000:
            break

    for tag in ['NOUN', 'VERB']:
        bigrams[tag] = nltk.FreqDist(bigrams[tag])

    for pos in bigrams:
        for k in bigrams[pos]:
            bigrams[pos][k] = math.log(bigrams[pos][k])


with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    counter = 0
    for line in infile:
        if counter >= 120000:
            ## outfile.write(line)
            #continue
            break

        if len(line.rstrip("\n").split()) < 5:
            continue

        if random.choice([0, 1]):
            if nums['inv'] > 60000:
                # outfile.write(line)
                continue
            c_tokens, c_tree = helpers.process(line)
            words = [(word["form"], word["upostag"]) for word in c_tokens]

            c1, c2 = None, None
            for n, (word, tag) in enumerate(words[1:-1]):
                if tag in ['NOUN', 'VERB']:
                    p1 = bigrams[tag][(words[n], words[n + 1])]
                    p2 = bigrams[tag][(words[n + 1], words[n + 2])]
                    c1 = set(
                        [
                            bigram[1][0]
                            for bigram in bigrams[tag]
                            if abs(bigrams[tag][bigram] - p1) <= 1
                        ]
                    )
                    c2 = set(
                        [
                            bigram[0][0]
                            for bigram in bigrams[tag]
                            if abs(bigrams[tag][bigram] - p2) <= 1
                        ]
                    )
                    break

            if not c1 or not c2:
                # outfile.write(line)
                continue

            candidates = c1.intersection(c2)
            if word in candidates:
                candidates.remove(word)

            if not candidates:
                # outfile.write(line)
                continue
            

            new_word = random.choice(list(candidates))

            #filter if corpus frequency too low
            # if freq_dist[word] < 40 or freq_dist[word] > 4000 or freq_dist[new_word] < 40 or freq_dist[new_word] > 4000:
            #    # outfile.write(line)
            #    continue

            old_word = words[n + 1][0]
            words[n + 1] = (new_word, None)

            if counter < 100000:
                subs["train"].append((old_word, new_word))

            if counter >= 100000 and counter < 110000:
                if (old_word, new_word) in subs["train"]:
                    # outfile.write(line)
                    continue

                subs["val"].append((old_word, new_word))

            if counter >= 110000 and counter < 120000:
                if (old_word, new_word) in subs["train"] or (
                    old_word,
                    new_word
                ) in subs["val"]:
                    # outfile.write(line)
                    continue

            nums['inv'] += 1
            status = "Inv"

        else:
            if nums['orig'] > 60000:
                # outfile.write(line)
                continue

            nums['orig'] += 1
            status = "Orig"     

        counter += 1
        sys.stdout.write(
            "{}\t{}\n".format(" ".join([i[0] for i in words]), status)
        )

