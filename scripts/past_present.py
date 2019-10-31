import gzip
# TODO: check FD
import helpers
import pickle
import sys

# init stuff
existing = {"train": set(), "val": set()}
total = {'Pres': 0, 'Past': 0}
counter = 0

# load freqdist
with open(sys.argv[3], "rb") as ser:
    freq_dist = pickle.load(ser)

# main loop
with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        # we have enough sentences
        if counter >= 120000:
            # outfile.write(line)
            break

        c_tokens, c_tree = helpers.process(line)
        root = c_tree.token
        root_form = root['form']

        if (
            root_form not in freq_dist
            or freq_dist[root_form] < 100
            or freq_dist[root_form] > 50000
        ):
            # outfile.write(line)
            continue

        if not root['feats'] or 'Tense' not in root['feats']:
            # outfile.write(line)
            continue
        
        tense = root['feats']['Tense']            
        if tense not in ['Pres', 'Past']:
            # outfile.write(line)
            continue

        if counter < 100000:
            if total[tense] >= 100000 / 2:
                # outfile.write(line)
                continue
               
            total[tense] += 1
            existing["train"].update(root_form)

        if counter >= 100000 and counter < 110000:
            if total[tense] >= 110000 / 2:
                # outfile.write(line)
                continue

            if root_form in existing["train"]:
                # outfile.write(line)
                continue

            total[tense] += 1
            existing["val"].update(root_form)

        if counter >= 110000 and counter < 120000:
            if total[tense] >= 120000 / 2:
                # outfile.write(line)
                continue

            if root_form in existing["train"] or root_form in existing["val"]:
                # outfile.write(line)
                continue

            total[tense] += 1
        
        counter += 1
        sent = " ".join(i['form'] for i in c_tokens)

        sys.stdout.write("{}\t{}\n".format(sent, tense))
