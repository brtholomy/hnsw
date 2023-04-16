import click
from random import random, randint
from math import floor, log
import networkx as nx

import graphing


def Insert(HNSW: dict, q: int, maxk: int, efConstruction: int, mL: float):
    """
    Inserts element q into HNSW structure.

    Args:
        HNSW: multilayer graph
        q: new element
        maxk: maximum degree for each node per layer
        efConstruction: size of the dynamic candidate list
        mL: normalization factor for level generation
    """

    # set of the currently found nearest elements
    W = set()
    eP = EntrancePoint(HNSW)
    topL = TopLayer(HNSW)

    # new element's topmost layer: notice the normalization by mL
    layer_i = floor(-1 * log(random()) * mL)
    # ensure we don't exceed our allocated layers.
    layer_i = min(layer_i, topL)

    # The first phase searches [topL, layer_i) for an updated eP, closest to q
    for lc in range(topL, layer_i + 1, -1):
        layer = GetLayer(HNSW, lc)
        W = SearchLayer(layer, q, eP, ef=1)
        eP = Nearest(W, q)

    # Now searches [layer_i, 0) using the found eP
    for lc in range(min(topL, layer_i), -1, -1):
        layer = GetLayer(HNSW, lc)
        W = SearchLayer(layer, q, eP, efConstruction)
        neighbors = SelectNeighbors(q, W, maxk)
        AddEdges(layer, q, neighbors)

        # Shrink connections if needed
        for e in neighbors:
            e_neighbors = Neighborhood(layer, e)
            if len(e_neighbors) > maxk:
                e_new_edges = SelectNeighbors(e, e_neighbors, maxk)
                ShrinkEdges(layer, e, e_new_edges)

        eP = Nearest(W, q)
    SetEntrancePoint(HNSW, eP)


def SearchLayer(layer: nx.Graph, q: int, eP: int, ef: int) -> set:
    """
    Searches for nearest neighbors to query.

    Args:
        layer: nx.Graph instance
        q: new element
        eP: entrance point for this search
        efConstruction: size of the dynamic candidate list

    Returns:
        nearestN: ef closest neighbors to q
    """
    visited = set([eP])
    cands = set([eP])
    nearestN = set([eP])

    while cands:
        c = Nearest(cands, q)
        cands.remove(c)
        f = Furthest(nearestN, q)
        if Distance(c, q) > Distance(f, q):
            # all elements in nearestN are evaluated
            break

        # update candidates and nearestN
        for e in Neighborhood(layer, c):
            if e not in visited:
                visited.add(e)
                f = Furthest(nearestN, q)
                if Distance(e, q) < Distance(f, q) or len(nearestN) < ef:
                    cands.add(e)
                    nearestN.add(e)
                    if len(nearestN) > ef:
                        nearestN.remove(Furthest(nearestN, q))
    return nearestN


def SelectNeighbors(q: int, cands: set, M: int):
    """Note: this is the simplest possible version of this routine, and leaves
    out the distance scaling heuristic.
    """
    if q in cands:
        cands.remove(q)
    return sorted(cands, key=lambda x: Distance(x, q))[:M + 1]


def EntrancePoint(HNSW: dict):
    return HNSW["entrance"]


def SetEntrancePoint(HNSW: dict, eP: int):
    HNSW["entrance"] = eP


def GetLayer(HNSW: dict, lc: int):
    return HNSW["layers"][lc]


def TopLayer(HNSW: dict):
    return len(HNSW["layers"]) - 1


def Distance(u: int, v: int):
    return abs(u - v)


def Furthest(W: set, q: int):
    return max(W, key=lambda w: Distance(w, q))


def Nearest(W: set, q: int):
    return min(W, key=lambda w: Distance(w, q))


def Neighborhood(layer: nx.Graph, u: int):
    # Always return at least the anchor point
    if u not in layer:
        return (0,)
    return layer[u]


def AddEdges(layer: nx.Graph, u: int, neighbors: set):
    for n in neighbors:
        layer.add_edge(u, n)


def ShrinkEdges(layer: nx.Graph, u: int, new_edges: set):
    removes = [(u, n) for n in layer[u] if n not in new_edges]
    layer.remove_edges_from(removes)


def ConstructHNSW(layers: int, maxk: int, n: int, efConstruction: int, mL: float):
    HNSW = {
        "entrance": 0,
        # We seed the stack with a single 0 node in all layers.
        "layers": [graphing.Single() for _ in range(layers)],
    }
    for _ in range(n):
        q = randint(0,n)
        Insert(HNSW, q, maxk, efConstruction, mL)
    return HNSW


@click.command()
@click.option(
    '--layers', '-l',
    default=10,
    show_default=True,
    help='number of hierarchical layers'
)
@click.option(
    '--maxk', '-k',
    default=5,
    show_default=True,
    help='max degree per node'
)
@click.option(
    '--nodes', '-n',
    default=20,
    show_default=True,
    help='number of nodes to insert'
)
@click.option(
    '--ef',
    default=5,
    show_default=True,
    help='max size of the candidate set during search'
)
@click.option(
    '--ml',
    default=3.0,
    show_default=True,
    help='normalization factor for probability of inserting nodes at subsequent levels'
)
@click.option(
    '--display', '-d',
    is_flag=True,
    show_default=True,
    help='whether to display the graphs using plt.Show()'
)
@click.option(
    '--save/--nosave',
    is_flag=True,
    show_default=True,
    default=True,
    help='whether to save the graphs as .png files to disk'
)
def Main(layers, maxk, nodes, ef, ml, display, save):
    HNSW = ConstructHNSW(layers, maxk, nodes, ef, ml)

    if display:
        for g in HNSW['layers']:
            graphing.DrawGraph(g)
            graphing.PlotShow()

    if save:
        for n, g in enumerate(HNSW['layers']):
            graphing.SaveGraph(g, 'hnsw', n)


if __name__ == "__main__":
    Main()
