from Heap import Heap, Node

class Vertex:
    def __init__(self, name, x_pos,y_pos):
        self.name = name
        self.y = y_pos
        self.x = x_pos


def dijkstra (G, start , end ):
    visited = set()
    path ={}

    h = Heap(len(G))
    nodeCosts ={}
    for n in G:
        nodeCosts[n] =float("inf")

    nodeCosts[start] =0  
    h.insert(Node( 0 ,start))
    while h.get_size() >= 0:
        node = h.remove()
        visited.add(node.point)

        if node.point ==end :
            break
        for Nodee, weight in G[node.point]:
            if Nodee in visited:
                continue

            newCost = nodeCosts[node.point] + weight
            if nodeCosts[Nodee] > newCost:
                path[Nodee] = node.point
                nodeCosts[Nodee] = newCost
                h.insert(Node(newCost, Nodee))
    # index2 = list(path).index(end)    
    f=[]
    if nodeCosts[end] !=    float("inf"):
        pr=end
        f.append(pr)
        while pr !=start:
            f.append(path[pr])
            pr=path[pr]

    return f, nodeCosts[end]

  