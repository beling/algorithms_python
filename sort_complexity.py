
import matplotlib.pyplot as plt
from random import randrange
from copy import copy

def min_index(tab, start = 0):
    global it
    res = start
    for i in range(start+1, len(tab)):
        it += 1
        if tab[i] < tab[res]:
            res = i
    return res

def sort_by_min(tab):
    for start in range(len(tab)):
        m = min_index(tab, start)
        tab[start], tab[m] = tab[m], tab[start]
       
def merge(A, B):
    global it
    res = []
    a = 0
    b = 0
    while a < len(A) and b < len(B):
        it += 1
        if A[a] <= B[b]:
            res.append(A[a])
            a += 1
        else:
            res.append(B[b])
            b += 1
    for i in range(a, len(A)):
        res.append(A[i])
    for i in range(b, len(B)):
        res.append(B[i])
    return res

def merge_sort(tab):
    if len(tab) <= 1: return tab
    mid = len(tab) // 2
    return merge(
        merge_sort(tab[:mid]),
        merge_sort(tab[mid:])
    )

def count_sort(tab):
    global it
    count = [0] * 1001
    for v in tab:
        it += 1
        count[v] += 1
    res = []
    for v in range(1001):
        for _ in range(count[v]):
            res.append(v)
    return res

def binary_search(T, e):
    start = 0
    end = len(T)
    while start < end:
        mid = start + (end - start) // 2
        if T[mid] == e: return mid
        if T[mid] > e:
            end = mid
        else:
            start = mid+1
    return -1

X = []
Y = []
Ymerge = []
Ycount = []
tab = []
for tab_size in range(1, 100):
    tab.append(randrange(0, 1001))
    X.append(len(tab))
    it = 0
    sort_by_min(copy(tab))
    Y.append(it)
    it = 0
    merge_sort(tab)
    Ymerge.append(it)
    it = 0
    count_sort(tab)
    Ycount.append(it)

plt.plot(X, Y, label='sort by swapping with minimum')
plt.plot(X, Ymerge, label='merge sort')
plt.plot(X, Ycount, label='count sort')
plt.legend(loc="upper left")
plt.show()
