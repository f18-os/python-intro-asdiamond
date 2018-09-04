import sys
import re
from collections import defaultdict


def usage():
    print(len(sys.argv))
    print("Correct usage is: python wordCount.py <inFile> <outFile>")
    exit()


if len(sys.argv) is not 3:
    usage()

inFile = sys.argv[1]
outFile = sys.argv[2]

# TODO need to close this file...
data = open(inFile, 'r').read().lower()
words = re.findall('\w+', data)

wordFrequency = defaultdict(int)
for word in words:
    wordFrequency[word] += 1

with open(outFile, 'w') as fp:
    for key in sorted(wordFrequency):
        fp.write(f"{key} {wordFrequency[key]}\n")
