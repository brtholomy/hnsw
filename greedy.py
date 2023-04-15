import graphing
import networkx as nx


# simplest possible definition: 1-dimensional vectors.
def Distance(q, v):
    return abs(q - v)


def GreedySearch(G, q, venter):
    vcurr = venter
    σmin= Distance(q, vcurr)
    vnext = None
    for vfriend in nx.neighbors(G, vcurr):
        if σfriend := Distance(q, vfriend) < σmin:
            σmin = σfriend
            vnext = vfriend
    if vnext == None:
        return vcurr
    else:
        return GreedySearch(G, q, vnext)


if __name__ == '__main__':
    G = graphing.MakeRingLattice(n=40, d=4)
    p = 0.2
    graphing.Rewire(G, p)
    # # G = random_g.make_random_graph(16,0.2)

    q = 20
    venter = 0
    res = GreedySearch(G, q, venter)
    print(f'{res = }')
