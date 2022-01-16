#!/usr/bin/env python3
# Piotr Beling, 2018

class FindUnionTree:
    """Tree implementation of find-union set. See:
    'Introduction to Algorithms' by Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein"""
    
    def __init__(self):
        """Construct one-element tree."""
        self.parent = None  # parent is None only for the root
        self.h = 0
        
    #@property
    #def root(self) -> 'FindUnionTree':
    #    if self.parent is None:
    #        return self
    #    result = self.parent.root
    #    self.parent = result
    #    return result
    
    @property
    def root(self) -> 'FindUnionTree':
        """Return the root of self and compress the path from self to its root."""
        result = self
        path = []   # path from self (included) to the root (excluded)
        while result.parent is not None:
            path.append(result)
            result = result.parent
        for node in path:   # path compression
            node.parent = result
        return result
    
    def in_same_set(self, other: 'FindUnionTree') -> bool:
        """Return whether self and other are in the same tree (set). Compress the paths from self and other to their roots."""
        return self.root is other.root
    
    def union(self, other: 'FindUnionTree') -> None:
        """Merge the sets which includes self and other by joining the root of the shorter tree to the root of the taller tree.
        Compress the paths from self and other to their roots."""
        self_root = self.root
        other_root = other.root
        if self_root is other_root: return
        if self_root.h >= other_root.h:
            other_root.parent = self_root
            if self_root.h == other_root.h:
                self_root.h += 1
            del other_root.h
        else:
            self_root.parent = other_root
            del self_root.h


if __name__ == "__main__":	# demo program:
    from random import randint
    tab = [FindUnionTree() for _ in range(20)]
    for _ in range(20):
        a = randint(0, 19)
        b = randint(0, 19)
        print("Are {} and {} in the same set? {}".format(a, b, tab[a].in_same_set(tab[b])))
        print("union {} and {}".format(a, b))
        tab[a].union(tab[b])

