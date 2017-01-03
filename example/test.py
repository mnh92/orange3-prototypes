import collections
import math
#from matplotlib import cm
#import pylab
import Orange

f = open("Escherichia coli.fasta")
s1 = f.read()
data = "".join(s1.split("\n")[1:])

#counts the k-mers
def count_kmers(sequence, k):
    count = collections.defaultdict(int)
    for i in range(len(data) - (k - 1)):
        count[sequence[i:i + k]] += 1
    return count

#calculates probabilities of k-mers
def probabilities(kmer_count, k):
    probabilities = collections.defaultdict(float)
    N = len(data)
    for key, value in kmer_count.items():
        probabilities[key] = float(value) / (N - k + 1)
    return probabilities

#calculates log-odds of k-mers
def logodds(kmer_count, k):
    logodd = collections.defaultdict(float)
    N = len(data)
    for key, value in kmer_count.items():
        logodd[key] = math.log((value / (N - k + 1)))
    return logodd


#visualizes the results
def chaos_game(probabilities, k):
    array_size = int(math.sqrt(4 ** k))
    chaos = []
    for i in range(array_size):
        chaos.append([0] * array_size)

    maxX = maxY = array_size
    posX = posY = 1
    for key, value in probabilities.items():
        for char in key:
            if char == "T":
                posX += maxX / 2
            elif char == "C":
                posY += maxY / 2
            elif char == "G":
                posX += maxX / 2
                posY += maxY / 2
            maxX = maxX / 2
            maxY /= 2
        chaos[int(posY - 1)][int(posX - 1)] = value
        maxX = maxY = array_size
        posX = posY = 1

    return chaos

"""
f3 = count_kmers(data, 3)
f4 = count_kmers(data, 6)


f3_prob = probabilities(f3, 3)
f4_prob = probabilities(f4, 6)

f3_log = logodds(f3, 3)
f4_log = logodds(f4, 6)


chaos_k4 = chaos_game(f4, 6)
pylab.title('Chaos game representation for 6-mers')
pylab.imshow(chaos_k4, interpolation='nearest', cmap=cm.gray_r)
pylab.show()

"""

"""

chaos_k3 = chaos_game(f3_prob, 3)
pylab.title('Chaos game representation for 3-mers')
pylab.imshow(chaos_k3, interpolation='nearest', cmap=cm.gray_r)
pylab.show()


print(f3)
print(f4)
print(f3_prob)
print(f4_prob)
print(f3_log)
print(f4_log)
"""

with open('test_file.csv') as file:
    data = Orange.data.Table('test_file.csv')

    print(data)

