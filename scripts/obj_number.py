import gzip
# TODO: check fd
import pickle
import sys
import helpers

# load freqdist
with open(sys.argv[3], "rb") as ser:
    freq_dist = pickle.load(ser)

# build test last
classes = {'train': {'Sing': 0, 'Plur': 0}, 
           'val': {'Sing': 0, 'Plur': 0}, 
           'test': {'Sing': 0, 'Plur': 0}}
words_seen = {"train": set(), "val": set()}
counter = 0

with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        # extra just in case
        if counter >= 120000:
            # outfile.write(line)
            break

        c_tokens, c_tree = helpers.process(line)

        subj_word = [
            i.token for i in c_tree.children if i.token["deprel"] == "obj"
        ]

        # reject if no/too many subjects
        if len(subj_word) != 1:
            # outfile.write(line)
            continue

        subj_word = subj_word[0]

        # reject if subject has no number
        if not subj_word["feats"] or "Number" not in subj_word["feats"]:
            # outfile.write(line)
            continue

        # reject if subject not frequent enough
        # TODO: tune
        if (
            subj_word["form"] not in freq_dist
            or freq_dist[subj_word["form"]] < 100
            or freq_dist[subj_word["form"]] > 50000
        ):
            # outfile.write(line)
            continue

        number = subj_word["feats"]["Number"]
        if number not in ['Sing', 'Plur']:
            continue

        word_form = subj_word["form"]

        # train
        if counter < 100000:
            if classes['train'][number] > 50000:
                # outfile.write(line)
                continue

            words_seen["train"].update([word_form])
            classes['train'][number] += 1
            counter += 1

        elif counter >= 100000 and counter < 110000:
            # reject if word form in train
            if word_form in words_seen["train"]:
                # outfile.write(line)
                continue

            if classes['val'][number] > 5000:
                # outfile.write(line)
                continue

            words_seen["val"].update([word_form])
            classes['val'][number] += 1
            counter += 1

        else:
            # reject if word form in train or val
            if (
                word_form in words_seen["train"]
                or word_form in words_seen["val"]
            ):
                # outfile.write(line)
                continue

            if classes['test'][number] > 5000:
                # outfile.write(line)
                continue


            classes['test'][number] += 1
            counter += 1

        sent = " ".join(i["form"] for i in c_tokens)
        sys.stdout.write("{}\t{}\n".format(sent, number))
