import gzip
from nltk import FreqDist
import sys
import pickle

lines = 0
with open(sys.argv[1], "r", errors="ignore") as f, open(sys.argv[2], "wb") as ser:
    fd = FreqDist()
    for line in f:
        line = line.rstrip("\n").split()
        fd.update(line)

    pickle.dump(fd, ser)
