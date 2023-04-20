import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def MakeRingLattice(n, d):
    offsets = range(1, (d//2) + 1)
    return nx.circulant_graph(n, offsets)


def Single():
    G = nx.Graph()
    G.add_node(0)
    return G


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
    plt.savefig(f'img/{prefix}_layer_{n}.png')
    plt.close()
