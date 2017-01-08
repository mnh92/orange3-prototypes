Introduction to Bioinformatics, Student project 2016/17 - Chaos Game Representation
===================================================================================

The properties of sequences can often be discovered by means of visualization.
This is an implementation of a prototype widget that visualizes the sequences.

The Chaos Game Representation
-----------------------------

The Chaos Game Representation (CGR) is a method that visualizes one-dimensional data
in a two dimensional image. It was first proposed by [H. Joel Jeffrey in 1990](http://nar.oxfordjournals.org/content/18/8/2163.full.pdf+html).

In the case of genome data, the CGR image displays the abundance of
all k-mers in a genome string for a chosen k. The image contains
4<sup>k</sup> boxes in a grid, each representing a specific k-mer. The
boxes are colored from white, meaning this k-mer is not present, to
black, meaning this k-mer is the most abundant.

Each k-mer is positioned in the image according to the following
algorithm: For each character in a k-mer, the image is subdivided into
four quadrants, with A in the top left, G in the top right, C in the
bottom left and T in the bottom right. Each quadrant is split
according to the same principle for the next character in the k-mer,
recursively, which can be seen in the next picture:

![alt tag](http://i.imgur.com/L4Wr3sz.png )

The k-mers in the given sequence are counted and the image is colored accordingly.
For example, here is a part of the 6-mer Chaos Game Representation, where the 6-mer
ATAAAA with the score 912 is the most abundant and the 6-mer AGCCCG with the score 3 is the least abundant:

![alt tag](https://bostjan-cigan.com/wp-content/uploads/2016/05/kmer_table_.png)

The Widget
----------

We implemented our widget in [Orange](http://orange.biolab.si/). It uses the Chaos Game Representation (CGR) to visualize genome data.
It accepts a file that contains the string of the genome sequence as input and then visualizes it with the [pyqtgraph](http://www.pyqtgraph.org/) library.

The GUI consists of two control panels on the left. One is for setting the k-mer length and counting scheme, 
the other one is for displaying the coordinates, sequence and value of each k-mer as the user hovers over it with the mouse.
The image representing the visualization of the sequence is in the center of the widget. On the right, the legend
shows which values are represented with which color. In the next image showing the widget's GUI, the user hovered over
the k-mer ATCT, which has the coordinates (7,5), the value of 0.00483 and is thus colored with the shade of gray seen in the legend.

![alt tag](http://i.imgur.com/LBtWmzl.jpg)

Setting the k-mer length changes the length (k) of the k-mers being
counted. A higher k will produce an image with more cells.

The widget allows three different counting schemes that determine how
the value of each cell in the image is calculated:

* raw count - The cells are colored according to the number of
  instances of each k-mer found.
* probability - The cells are colored according to the probability of
  each k-mer.
* log odds - The cells are colored according to the logarithm of the
  probability of each k-mer.

Note that all the first two counting methods produce the same image
with different scales, while the third empasizes the differences
between the counts.
