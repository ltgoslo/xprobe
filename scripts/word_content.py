import gzip
import sys
import pickle
import helpers

corpus = []
counter = 0

with open(sys.argv[3], "rb") as f:
    fd = pickle.load(f)

checklist = {}
total = 0
for word, freq in fd.most_common(10000)[2001:]:
    if total == 1000:
        break

    if len(word) >= 4 and word not in checklist:
        checklist[word] = 0
        total += 1

counter = 0
with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        if counter >= 120000:
            # outfile.write(line)
            break

        c_tokens, c_tree = helpers.process(line)

        word_counter = 0
        for word in c_tokens:
            if word['form'] in checklist:
                word_counter += 1
                current_word = word

        # reject if more than one of the words in sent
        if word_counter != 1:
            # outfile.write(line)
            continue

        checklist[current_word['form']] += 1
        # reject if too many of current class
        if checklist[current_word['form']] > 120:
            # outfile.write(line)
            continue

        else:
            counter += 1
            sys.stdout.write(
                "{}\t{}\n".format(" ".join([i['form'] for i in c_tokens]), current_word['form'])
            )
