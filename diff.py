#!/usr/bin/env python3
# Piotr Beling, 2024

from enum import Enum
import argparse

def glcs(P, lenA, lenB):
    '''Returns the generalized LCS (longest common subsequence) matrix
       (of size lenA+1 times lenB+1) for a function P such that P(a, b)
       is the similarity of the a-th A and the b-th B element,
       for 0<=a<lenA, 0<=b<lenB.'''
    t = [[0] * (lenB+1) for _ in range(lenA+1)]
    for a in range(lenA):
        for b in range(lenB):
            t[a+1][b+1] = max(t[a][b] + P(a, b), t[a][b+1], t[a+1][b])
    return t

def lcs(A, B):
    '''Returns the LCS (longest common subsequence) matrix for given sequences.'''
    return glcs(lambda a, b: A[a] == B[b], len(A), len(B))

def lcs_for_sim_matrix(P):
    '''Returns the LCS (longest common subsequence) matrix for given similarity matrix.'''
    return glcs(lambda a, b: P[a][b], len(P), len(P[0]))

def lines_of(filename):
    '''Returns the contents of a file as a list of strings with its lines.'''
    with open(filename, encoding="utf-8") as f:
        return f.read().splitlines()
    
class Diffs(Enum):
    OnlyA = 0   # element included only in A
    OnlyB = 1   # element included only in B
    Common = 2  # element included in both
    
def diff(lcs):
    """Returns a list of differences for given LCS (longest common subsequence) matrix."""
    changes = []
    a, b = len(lcs)-1, len(lcs[0])-1
    while a > 0 and b > 0:
        if lcs[a][b] == lcs[a-1][b]:
            changes.append(Diffs.OnlyA)
            a -= 1
        elif lcs[a][b] == lcs[a][b-1]:
            changes.append(Diffs.OnlyB)
            b -= 1
        else:
            changes.append(Diffs.Common)
            a -= 1
            b -= 1
    changes.extend(Diffs.OnlyA for _ in range(a))
    changes.extend(Diffs.OnlyB for _ in range(b))
    changes.reverse()
    return changes

def print_files_diff(diffs, A, B):
    '''Print differences for the given list of differences
       and compared sequences which are the lists of strings.'''
    a, b = 0, 0
    for d in diffs:
        if d == Diffs.OnlyA:
            print("\033[31m", A[a], sep='')
            a += 1
        elif d == Diffs.OnlyB:
            print("\033[32m", B[b], sep='')
            b += 1
        else:
            la, lb = A[a], B[b]
            print("\033[0m", end='')
            h = diff(lcs(la, lb))
            print_lines_diff(h, la, lb)
            print()
            a += 1
            b += 1
            
def print_lines_diff(diffs, A: str, B: str):
    '''Print differences for the given list of differences
       and compared sequences which are the strings.'''
    a, b = 0, 0
    prev_d = None
    for d in diffs:
        if d == Diffs.OnlyA:
            if d != prev_d: print("\033[31m", sep='', end='')
            print(A[a], sep='', end='')
            a += 1
        elif d == Diffs.OnlyB:
            if d != prev_d: print("\033[32m", sep='', end='')
            print(B[b], sep='', end='')
            b += 1
        else:
            if d != prev_d: print("\033[0m", sep='', end='')
            print(A[a], sep='', end='')
            a += 1
            b += 1
        prev_d = d
        
def sim_accurate(A, B):
    """Returns similarity of A and B in range [0, 1000000],
       calculated from length of their LCS."""
    if len(A) == 0: return int(A == B) * 1000000
    return lcs(A, B)[-1][-1] * 2000000 // (len(A)+len(B))

def sim_fast(A, B):
    """Returns similarity of A and B in range [0, 1000000],
       calculated from length of their common prefix and suffix."""
    if len(A) == 0 and len(B) == 0: return 1000000
    common = 0
    for i in range(min(len(A), len(B))):
        if A[i] != B[i]: break
        common += 1
    for i in range(1, 1+min(len(A), len(B))-common):
        if A[-i] != B[-i]: break
        common += 1
    return common * 2000000 // (len(A)+len(B))
         

parser = argparse.ArgumentParser(description='Print out the differences between the two files.')
parser.add_argument('-s', '--sim', choices=['accurate', 'fast'], default='accurate', metavar='f',
                    help="similarity function to use, 'accurate' (default) or 'fast'")
parser.add_argument("file1", help="name of the first file to compare")
parser.add_argument("file2", help="name of the second file to compare")
args = parser.parse_args()

A = lines_of(args.file1)
B = lines_of(args.file2)

if args.sim == 'fast':
    sim = sim_fast
else:
    sim = sim_accurate

P = [[sim(a, b) for b in B] for a in A]
print_files_diff(diff(lcs_for_sim_matrix(P)), A, B)