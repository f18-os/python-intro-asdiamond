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

    # the file will be closed when the buffered reader is gcd
    data = open(in_file, 'r').read().lower()
    words = re.findall('\w+', data)

    word_frequency = defaultdict(int)
    for word in words:
        word_frequency[word] += 1

    with open(out_file, 'w') as fp:
        for key in sorted(word_frequency):
            fp.write(f"{key} {word_frequency[key]}\n")


if __name__ == '__main__':
    main()
