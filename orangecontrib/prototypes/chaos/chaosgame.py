import collections
import math
import numpy as np


def raw_count(sequence, kmer_length):
    count = collections.defaultdict(int)
    for i in range(len(sequence) - (kmer_length - 1)):
        count[sequence[i:i + kmer_length]] += 1
    return count


def probabilities(sequence, kmer_length):
    probs = collections.defaultdict(float)
    l = len(sequence)
    counts = raw_count(sequence, kmer_length)
    for k, v in counts.items():
        probs[k] = float(v) / (l - kmer_length + 1)
    return probs


def log_odds(sequence, kmer_length):
    logOdd = collections.defaultdict(float)
    l = len(sequence)
    counts = raw_count(sequence, kmer_length)
    for k, v in counts.items():
        logOdd[k] = math.log((v / (l - kmer_length + 1)))
    return logOdd


def cgr(probabilities, kmer_length):
    size = int(math.sqrt(4 ** kmer_length))
    chaos = np.zeros((size, size))
    kmers = {}

    for kmer, prob in probabilities.items():
        x_max = size
        y_max = size
        x_pos = 0
        y_pos = 0

        for c in kmer:
            if c == 'G':
                x_pos += x_max / 2
            elif c == 'C':
                y_pos += y_max / 2
            elif c == 'T' or c == 'U':
                x_pos += x_max / 2
                y_pos += y_max / 2

            x_max /= 2
            y_max /= 2
        chaos[int(x_pos), int(y_pos)] = prob
        kmers[int(x_pos), int(y_pos)] = kmer
    return chaos, kmers
