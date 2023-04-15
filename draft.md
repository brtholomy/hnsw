# Introduction

---

The first thing to understand about HNSW, is that's primarily an optimized data structure, not an algorithm. Actually the algorithm used with these structures is remarkably simple: a greedy search which simply looks among all current candidates for the closest target value.

What's brilliant about HNSW therefore is not its search routine, but its optimized structure for a *decentralized similarity search* using a simple greedy traversal. This makes it ideal as the backbone for realtime search applications.

---

To understand HNSW, we need to unpack the term's historical layers as though it were Lisp or Polish notation: `(Hierarchical (Navigable (Small World)))`.

1. *Hierarchical*: referring to stacked subgraphs of exponentially decaying density, a structure which addresses the problem of high dimensionality.
1. *Navigable*: referring to the search complexity of the subgraphs, which achieve (poly)logarithmic scaling using a decentralized search algorithm.[1][navigability]
1. *Small World* : referring to a unique graph with low average shortest path length and a high clustering coefficient.

Thus we begin at the end: what's a "small world"?

---

# Small World

What is a "small world" (SW) graph? It's graph structure which achieves a unique balance between regularity and randomness, poised at the sweet spot in which the advantages of both can be achieved.

Ideally, what we want from a graphical structure in the context of a search routine, is the ability to find our goal efficiently no matter where we begin. This requires that we address these contingencies:

1. We're far from our goal. This requires that we travel far without excessive cost: in other words, that long-distance links across the graph can be found.

2. We're close to our goal. This requires that we travel short distances without too many steps: thus that short-distance links can be found.

Randomly connected graphs tend to have long-distance links.

Regular graphs tend to have many short-distance links.

---

For example, imagine you'd like to travel from Seal Point Park in San Mateo, California to Prospect Park in Brooklyn, New York. You could walk, ride a bike, drive, or take a personal helicopter in short trips. But even if you were driving, if the travel network were only locally connected it would require that you use only local roads between towns, and the trip would be highly inefficient.

In practice what we do is to navigate small highly clustered networks locally, find a hub with long distance links, and revert to local navigation again: we use our feet, then a car, then a train, then a plane, then a car, then our feet again. This is what small world graphs seek to emulate: it turns out that many features in nature and civilization can be modeled as a small world graph, with both a high *clustering coefficient* and a low *average shortest path*.

---

But what do these terms mean?

## Low average shortest path length

This simply means that the distance between any two given nodes is generally reasonable. To achieve this property, a graph must have a good distribution of long-distance edges: however, a balance is desireable, since too many edges will burden the greedy search inner loop, and too few will inflate our average path length.

---

## Clustering coefficient

The clustering coefficient is a measure of the degree of connectedness between nearby nodes, calculated as the ratio of actual edges to possible edges among the neighbors of any given node.

    The local clustering coefficient is computed as the proportion of connections among its neighbours which are actually realised compared with the number of all possible connections.

---

The interesting thing about SW graphs is that they achieve a balance between these desireable structural features:

1. Low average shortest path length (L) : random graphs achieve this
1. High clustering coefficient (C) : regular lattice graphs achieve this

Moreover, they can be constructed by either adding random connections to an ordered graph, or adding order to a random graph. Consulting the original 1998 paper by Watts and Strogatz on small world graphs, we read:

> These small-world networks result from the immediate drop in L(p) caused by the introduction of a few long-range edges. Such ‘short cuts’ connect vertices that would otherwise be much farther apart than Lrandom. For small p, each short cut has a highly nonlinear effect on L, contracting the distance not just between the pair of vertices that it connects, but between their immediate neighbourhoods

Only need a small amount of random connections to achieve much shorter L

---

# Navigable: Logarithmic search complexity

Achieving logarithmic search complexity is generally considered the grand prize of algorithmic efficiency.

---

Navigability: the ability to find a logarithmically short path between any two vertices using only local information.

> https://doi.org/10.1371%2Fjournal.pone.0158162


---

# What do we mean by greedy search?

Greedy search: "greedy" in the sense that only the *local* optimum is considered when finding the *global* optimum. There is no attempt to predict future outcomes nor learn from the past: the algorithm simply makes the best choice at every step. This kind of algorithm generally only works with orderly data structures and relatively uniform data, such as binary trees and sorted arrays - technically any problem with an optimal substructure.

Its advantage is its simplicity and robustness.

---

    The Watts and Strogatz model was designed as the simplest possible model that addresses the first of the two limitations. It accounts for clustering while retaining the short average path lengths of the ER model.

    Consequently, the model is able to at least partially explain the "small-world" phenomena in a variety of networks, such as the power grid, neural network of C. elegans, networks of movie actors, or fat-metabolism communication in budding yeast.

---

### Why polylogarithmic scaling of NSW

Why NSW isn't good enough.

    The reason for the polylogarithmic complexity scaling of a single greedy search in NSW is that the overall num- ber of distance computations is roughly proportional to a product of the average number of greedy algorithm hops by the average degree of the nodes on the greedy path. The average number of hops scales logarithmically [26, 44], while the average degree of the nodes on the greedy path also scales logarithmically due to the facts that: 1) the greedy search tends to go through the same hubs as the network grows [32, 44]; 2) the average num- ber of hub connections grows logarithmically with an increase of the network size. Thus we get an overall pol- ylogarithmic dependence of the resulting complexity.

---

But it turns out that an NSW graph isn't good enough. The weakness of NSW graphs is their polylogarithmic scaling: a greedy search must deal with something like O(logn^k) complexity, since the overall cost is roughly:

    (average number of nodes evaluated)*(average degree of nodes)

*Both* of which scale logarithmically as the graph grows, since the average *k* degree is greatly influenced by the number of "hub" nodes.

---

# Hierarchical

An HNSW structure is a set of replicated NSW graphs, which grow sparser and wider at every iteration. If you collapsed the layers, you'd have a single NSW graph again.

The idea is to solve the polylogarithmic scaling of NSW graphs by eliminating early iteration of all edges of highly connected hub nodes, keeping only the relevant long-range edges in the early stages of the search.

The genius of this idea is especially evident when one considers the simplicity of the mechanism required to create these layers: one need only separate

> For every element we select an integer level l which defines the maximum layer for which the element belongs to. For all elements in a layer a proximity graph (i.e. graph containing only “short” links that approximate Delaunay graph) is built incrementally. If we set an exponentially decaying probability of l (i.e. following a geometric distribution) we get a logarithmic scaling of the expected number of layers in the structure.

> The idea of Hierarchical NSW algorithm is to separate the links according to their length scale into different layers and then search in a multilayer graph. In this case we can evaluate only a needed fixed portion of the connec- tions for each element independently of the networks size, thus allowing a logarithmic scalability.

> malkov hnsw paper

---

Key features:

1. explicit selection of the graph’s entrance node
1. separation of links by different scales
1. use of an advanced heuristic to select the neighbors

> malkov hnsw paper

---

## Skip list

There is an important precedent for HNSW graphs: the "skip list". A skip list is a linked list ...

---


[navigability]: https://doi.org/10.48550/arXiv.1501.04931
