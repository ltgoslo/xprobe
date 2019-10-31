import gzip
import helpers
import random
import sys

# build test last
type_counter = {"l": 0, "b": 0, "r": 0}
classes = {'O': 0, 'I': 0}
counter = 0


def swap_consts(sent):
    cc = [word for word in sent if word['deprel'] == "cc"]
    assert len(cc) == 1, "Too many conjunctions!"
    cc = cc[0]

    # reject if conj is not top level
    t = sent.to_tree()
    root_id = t.token['id']
    assert len([i for i in t.children if i.token['deprel'] == 'conj']) == 1

    # get balancy type
    if cc["id"] * 2 == len(sent) + 1:
        typ = "b"

    elif cc["id"] * 2 < len(sent) - 1:
        typ = "l"

    else:
        typ = "r"

    start_buffer = []
    end_buffer = []
    start = False

    # uncapitalise
    sent[0]['form'] = sent[0]['form'].lower()

    for n, word in enumerate(sent):
        if start:
            if word['head'] == root_id and word['deprel'] != 'conj':
                end_buffer.append(word['form'])

            else:
                start_buffer.append(word['form'])

        if word == cc:
            start = True

    insert_point = len(start_buffer)
    start_buffer.append(cc['form'])

    for n, word in enumerate(sent):
        if word == cc:
            if n > 0 and sent[n-1]['deprel'] == 'punct':
                start_buffer = start_buffer[:-1]
                start_buffer.insert(insert_point, sent[n-1]['form'])

            break

        start_buffer.append(word['form'])

    start_buffer.extend(end_buffer)
    # fix caps
    start_buffer[0] = start_buffer[0].capitalize()
    return start_buffer, typ


with open(sys.argv[1], "r", errors="ignore") as infile, open(sys.argv[2], "w", errors="ignore") as outfile:
    for line in infile:
        # reject if enough sents
        if counter >= 120000:
            # outfile.write(line)
            break

        c_tokens, c_tree = helpers.process(line)

        try:
            swapped, typ = swap_consts(c_tokens)
        except AssertionError:
            # outfile.write(line)
            continue

        # reject if type is full
        if type_counter[typ] >= 120000 / 3:
            # outfile.write(line)
            continue

        type_counter[typ] += 1

        if random.choice([0, 1]):
            words = swapped
            status = "I"
        else:
            words = [word['form'] for word in c_tokens]
            words[0] = words[0].capitalize()
            status = "O"

        if classes[status] > 60000:
            # outfile.write(line)
            continue

        counter += 1
        sys.stdout.write("{}\t{}\n".format(" ".join(words), status))
