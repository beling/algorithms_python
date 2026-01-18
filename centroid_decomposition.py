#!/usr/bin/env python3
# Piotr Beling, 2026

class Tree:
   
    def __init__(self, vert_count):
        self.adj = [[] for _ in range(vert_count)]
        self._subtree_size = [0] * vert_count
        self._removed = [False] * vert_count
       
    def add_edge(self, a, b):
        self.adj[a].append(b)
        self.adj[b].append(a)
       
    def vert_count(self):
        return len(self.adj)
   
    def subtree_sizes(self, start):
        def _subtree_sizes(v):
            res = 1
            self._removed[v] = True
            for a in self.adj[v]:
                if not self._removed[a]:
                    res += _subtree_sizes(a)
            self._removed[v] = False
            self._subtree_size[v] = res
            return res
        return _subtree_sizes(start)
   
    def centroid(self, v):
        vert_num = self.subtree_sizes(v)
        prev = -1
        while True:
            for a in self.adj[v]:
                if a == prev or self._removed[a]: continue
                if self._subtree_size[a] * 2 > vert_num:
                    prev = v
                    v = a
                    break
            else:
                return v
           
    def shortest_paths(self, start, out_tab):
        def _shortest_paths(v, dist):
            out_tab[v].append((start, dist))
            dist += 1
            self._removed[v] = True
            for a in self.adj[v]:
                if not self._removed[a]:
                    _shortest_paths(a, dist)
            self._removed[v] = False
        _shortest_paths(start, 0)
       
    def centroid_decomp(self):
        def _centroid_decomp(start):
            c = self.centroid(start)
            self.shortest_paths(c, out_tab)
            self._removed[c] = True
            for a in self.adj[c]:
                if not self._removed[a]:
                    _centroid_decomp(a)
            self._removed[c] = False
       
        out_tab = [[] for _ in range(tree.vert_count())]
        _centroid_decomp(0)
        return CentroidDecomp(out_tab)
   
class CentroidDecomp:
    def __init__(self, decomb):
        self.decomb = decomb
       
    def dist(self, a, b):
        """Returns the shortest distance from a to b."""
        for (c1, d1), (c2, d2) in zip(self.decomb[a], self.decomb[b]):
            if c1 != c2: break # impossible in the first iteration
            result = d1 + d2 # length of the route: a -> common centroid -> b
        return result


if __name__ == "__main__":	# demo program:
    tree = Tree(5)
    tree.add_edge(0, 1)
    tree.add_edge(1, 2)
    tree.add_edge(2, 3)
    tree.add_edge(3, 4)

    d=tree.centroid_decomp()
    print(d.dist(0, 4))