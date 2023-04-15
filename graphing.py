import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def MakeRingLattice(n, d):
    offsets = range(1, (d//2) + 1)
    return nx.circulant_graph(n, offsets)

# https://eng.libretexts.org/Bookshelves/Computer_Science/Applied_Programming/Book%3A_Think_Complexity%3A_Exploring_Complexity_Science_with_Python_(Downey)/03%3A_Small_World_Graphs/3.04%3A_WS_graphs

# Adapted from "Think Complexity", 3.4: WS graphs

def Rewire(G, p):
    all_nodes = set(G)
    for u, v in G.edges():
        if np.random.random() < p:
            u_connections = set([u]) | set(G[u])
            choices = all_nodes - u_connections
            new_v = np.random.choice(list(choices))
            G.remove_edge(u, v)
            G.add_edge(u, new_v)


def MakeNSW(n=20, d=4, p=0.2):
    G = MakeRingLattice(n, d)
    Rewire(G, p)
    return G


def Empty(n):
    return nx.empty_graph(n)


def Single():
    G = nx.Graph()
    G.add_node(0)
    return G


def RemoveIsolates(G):
    G.remove_nodes_from(list(nx.isolates(G)))


def DrawGraph(G):
    options = {
        "font_size": 12,
        "node_size": 500,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 4,
        "width": 2,
        "with_labels": True,
    }
    nx.draw_circular(G, **options)


def PlotShow():
    # special magic for avoiding a blocking call
    plt.show(block=False)
    # Pause to allow the input call to run:
    plt.pause(0.001)
    input("hit [enter] to end.")
    plt.close('all')


def SaveGraph(G, prefix='', n=0):
    DrawGraph(G)
    plt.savefig(f'figures/{prefix}_layer_{n}.png')
    plt.close()


if __name__ == '__main__':
    G = MakeRingLattice(n=20, d=4)
    p = 0.2
    Rewire(G, p)
    nx.draw_circular(G)
    PlotShow()
