import collections
import math
import numpy as np


def raw_count(sequence, kmer_length):
    count = collections.defaultdict(int)
    for i in range(len(sequence) - (kmer_length - 1)):
        count[sequence[i:i + kmer_length]] += 1
    return count


def probabilities(sequence, kmer_length):
    pass


def log_odds(sequence, kmer_length):
    pass


def cgr(probabilities, kmer_length):
    size = int(math.sqrt(4 ** kmer_length))
    chaos = np.zeros((size, size))

    for kmer, prob in probabilities.items():
        x_max = size
        y_max = size
        x_pos = 1
        y_pos = 1

        for c in kmer:
            if c == 'T':
                x_pos += x_max / 2
            elif c == 'C':
                y_pos += y_max / 2
            elif c == 'G':
                x_pos += x_max / 2
                y_pos += y_max / 2

            x_max /= 2
            y_max /= 2
        chaos[int(x_pos) - 1, int(y_pos) - 1] = prob
    return chaos
