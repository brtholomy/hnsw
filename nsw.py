import click
import networkx as nx
import numpy as np

import graphing


def MakeNSW(n: int=20, d: int=4, p:float=0.2) -> nx.Graph:
    G = graphing.MakeRingLattice(n, d)
    Rewire(G, p)
    return G


# Adapted from "Think Complexity", 3.4: WS graphs by Allen B. Downey
def Rewire(G: nx.Graph, p: float):
    all_nodes = set(G)
    for u, v in G.edges():
        if np.random.random() < p:
            u_connections = set([u]) | set(G[u])
            choices = all_nodes - u_connections
            new_v = np.random.choice(list(choices))
            G.remove_edge(u, v)
            G.add_edge(u, new_v)


@click.command()
@click.option(
    '--nodes', '-n',
    default=20,
    show_default=True,
    help='number of nodes'
)
@click.option(
    '--degree', '-k',
    default=4,
    show_default=True,
    help='degree of nodes'
)
@click.option(
    '--prob', '-p',
    default=0.2,
    show_default=True,
    help='probability of rearranging edges'
)
@click.option(
    '--display', '-d',
    is_flag=True,
    help='whether to display the graphs'
)
@click.option(
    '--save', '-s',
    is_flag=True,
    help='whether to save the graphs as .png files'
)
def Main(nodes, degree, prob, display, save):
    G = MakeNSW(nodes, degree, prob)

    if display:
        graphing.DrawGraph(G)
        graphing.PlotShow()

    if save:
        graphing.SaveGraph(G, prefix='nsw')


if __name__ == '__main__':
    Main()
