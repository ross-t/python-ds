#python-ds
A collection of sample data structures and algorithms implemented in Python. The intention isn't that you should use these in production, it's for you to learn from them (and trust me, they're not perfect; many are intentionally simplified to make them more easily understandable, even when it sacrifices proper details and makes performance worse)


#Graphs
[graphpaths.py](Graphs/graphs.py) requires numpy. It's an implementation of Floyd-Warshall and Kruskal's algorithms. You can use it to generate random simple graphs and it has the (limited) ability to create files readable by graphviz, but only under some circumstances (and it desperately needs cleaning up). If you actually need to work with graphs in Python, I recommend using [networkx](https://networkx.github.io/).

There's a disjoint set in there, too.

[simplegraph.py](Graphs/simplegraph.py) is a basic adjacency-list graph implementation with reference implementations of depth and breadth-first search. It also demonstrates how to find components of a graph.

#Matrices
[MatrixChainMultiplication.py](Matrices/MatrixChainMultiplication.py) is a dynamic programming solution to the matrix chain multiplication problem. It requires numpy.

#Sorting
[mergesort.py](Sorting/mergesort.py) is mergesort. Surprise!

[quicksort.py](Sorting/quicksort.py) is quicksort. Surprise again!

#Tables
[hashtable.py](Tables/hashtable.py) is a simple hash table implementation.

#Trees
[splay_tree.py](Trees/splay_tree.py) implements a key-value storage splay tree.
[binaryheap.py](Trees/binaryheap.py) is a min-heap implemented with array storage.