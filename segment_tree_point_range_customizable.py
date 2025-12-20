
class SegmentTree:
   
    def _calc_node(self, i):
        left = 2*i
        self.data[i] = self.f(self.data[left], self.data[left+1])
   
    def __init__(self, tab, f=lambda l,r: l+r, zero=0):
        self.f = f
        self.zero = zero
        h = (len(tab)-1).bit_length()
        self.n = 1 << h # self.n = 2 ** h
        self.data = [zero] * (2 * self.n)
        #self.data[self.n:self.n+len(tab)] = tab
        for i, v in enumerate(tab): self.data[i+self.n] = v
        for i in range(self.n-1, 0, -1): self._calc_node(i)

    def _leaf_index(self, i):
        if i < 0:
            i += len(self.data)
        else:
            i += self.n    
        if i >= len(self.data) or i < self.n:
            raise IndexError('SegmentTree index out of range')
        return i

    def __setitem__(self, i, v):
        i = self._leaf_index(i)
        self.data[i] = v
        i //= 2
        while i > 0:
            self._calc_node(i)
            i //= 2
           
    def __getitem__(self, i):
        return self.data[self._leaf_index(i)]
   
    def __str__(self):
        return str(self.data[self.n:])
   
    def __repr__(self):
        return f'SegmentTree({self}, ???)'
   
    def __len__(self):
        return len(self.data) - self.n
   
    def __iter__(self):
        for i in range(self.n, len(self.data)):
            yield self.data[i]
   
    def total(self):
        return self.data[1]
   
    def in_range(self, l, r):
        res_l = self.zero
        res_r = self.zero
        l = self._leaf_index(l) - 1
        r = self._leaf_index(r) + 1
        while l // 2 != r // 2:
            if l % 2 == 0: res_l = self.f(res_l, self.data[l+1])
            if r % 2 == 1: res_r = self.f(self.data[r-1], res_r)
            l //= 2
            r //= 2
        return self.f(res_l, res_r)
