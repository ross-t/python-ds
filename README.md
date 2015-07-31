#python-ds
A collection of sample data structures and algorithms implemented in Python. The intention isn't that you should use these in production, it's for you to learn from them (and trust me, they're not perfect -- in fact, they're meant to be simple implementations you can use to help understand them!)

[graphs.py](graphs.py) requires numpy. It uses an adjacency-list graph implementation to implement Floyd-Warshall and Kruskal's algorithm. It can generate random simple graphs and has the (limited) ability to create files readable by graphviz. If you actually need to work with graphs in Python, I recommend using [networkx](https://networkx.github.io/).

There's a disjoint set in there, too.

[hashtable.py](hashtable.py) is a simple hash table implementation.

[splay_tree.py](splay_tree.py) implements a key-value storage splay tree.
