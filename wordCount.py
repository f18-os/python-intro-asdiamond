import sys
import re
from collections import defaultdict


def usage():
    print(len(sys.argv))
    print("Correct usage is: python wordCount.py <inFile> <outFile>")
    exit()


def main():
    if len(sys.argv) is not 3:
        usage()

    in_file = sys.argv[1]
    out_file = sys.argv[2]

    # TODO need to close this file...
    data = open(in_file, 'r').read().lower()
    words = re.findall('\w+', data)

    wordFrequency = defaultdict(int)
    for word in words:
        wordFrequency[word] += 1

    with open(out_file, 'w') as fp:
        for key in sorted(wordFrequency):
            fp.write(f"{key} {wordFrequency[key]}\n")


if __name__ == '__main__':
    main()
