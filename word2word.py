#!/usr/bin/env python3
# Piotr Beling, 2024

from array import array
from sys import argv

if not (3 <= len(argv) <= 4):
    print(f'usage: {argv[0]} word1 word2 [dictionary_file]')
    exit()

word1 = argv[1]
word2 = argv[2]
try:
    dict_file_name = argv[3]
except IndexError:
    dict_file_name = '/usr/share/dict/words'

n = len(word1)
if len(word2) != n:
    print(f'words differ in length: {n} != {len(word2)}')
    exit()

lower = word1.islower() and word2.islower()
if not lower:
    if not (word1.isupper() and word2.isupper()):
        print('mix of upper and lower case')
        exit()

if word1 == word2:
    print('the words are the same')
    exit()

words = set()
alphabet = set()

def add_word(word):
    words.add(word)
    alphabet.update(word)

with open(dict_file_name) as f:
    for word in f:
        word = word.strip()
        word = word.lower() if lower else word.upper()
        if len(word) == n: add_word(word)
add_word(word1)
add_word(word2)
alphabet = ''.join(alphabet)

def neighbors(word):
    result = array('u', word)   #result = list(word)
    for i, c in enumerate(word):
        for a in alphabet:
            if a != c:
                result[i] = a
                r = result.tounicode()  #r = ''.join(result)
                if r in words: yield r
        result[i] = c

def print_res(level: int, result: list[str] = []):
    if level == 0:
        if result: print(' -> '.join(reversed(result)))
    else:
        try:
            w = result[-1]
        except IndexError:
            w = word2
        for n in neighbors(w):
            if n in levels[level]:
                result.append(n)
                print_res(level-1)
                result.pop()

levels = []
P = set()
C = {word1}
F = set()
while C:
    levels.append(C)
    for c in C:
        for n in neighbors(c):
            if n == word2:
                print(word1, '->')
                print_res(len(levels)-1)
                print('->', word2)
                exit()
            if not (n in P or n in C):
                F.add(n)
    P = C
    C = F
    F = set()
print('no solution')
