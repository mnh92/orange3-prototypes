Introduction to Bioinformatics, Student project 2016/17 - Chaos Game Representation
===================================================================================

The properties of sequences can often be discovered by means of visualization.
This is an implementation of a prototype widget that visualizes the sequences.

The Chaos Game Representation
-----------------------------

This widget uses the Chaos Game Representation (CGR) to visualize
genome data. The CGR is a method that visualizes one-dimensional data
in a two dimensional image. It was first proposed by
[H. Joel Jeffrey in 1990]
(http://nar.oxfordjournals.org/content/18/8/2163.full.pdf+html).

In the case of genome data, the CGR image displays the abundance of
all k-mers in a genome string for a chosen k. The image contains
k<sup>4</sup> boxes in a grid, each representing a specific k-mer. The
boxes are colored from white, meaning this k-mer is not present, to
black, meaning this k-mer is the most abundant.

_mogoče tukaj beseda o nastavitvah widgeta, verjetnost, število, log
odds in to..._

The each k-mer is positioned on the image according to the following
algorithm:

For each letter in a k-mer, the image is subdivided into four
quadrants, with A in the top left, G in the top right, C in the
bottom left and T in the bottom right. Each quadrant is split
according to the same principle for the next letter in the k-mer,
recursively.

_tukaj primer CGRja_
