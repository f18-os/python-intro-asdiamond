import sys
import re
from collections import defaultdict


def usage():
    print(len(sys.argv))
    print("Correct usage is: python wordCount.py <input> <output>")


if len(sys.argv) is not 3:
    usage()
    exit()

inFile = sys.argv[1]
outFile = sys.argv[2]

# this one didnt have weird side effect where ; , and . were there own words...
expr = re.compile(':*;*\.*,*\s+')

# 0 or more (';' or ',' or '.') followed by 1 or more spaces
# expr = re.compile('([;,.:])*\s+')
wordFrequency = defaultdict(int)

with open(inFile, 'r') as fp:
    for word in expr.split(fp.read()):
        if word is None:
            continue
        wordFrequency[word.lower()] += 1

for key in sorted(wordFrequency):
    print(f"{key} {wordFrequency[key]}")
