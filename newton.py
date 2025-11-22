def newton_recc(n, k):
    if k == 0: return 1
    return n * newton_recc(n-1, k-1) // k

def newton_rec(n, k):
    return newton_recc(n, min(k, n-k))

def newton_iter(n, k):
    k = min(k, n-k)
    w = 1
    for i in range(1, k+1):
        w = (n - k + i) * w // i
    return w

def newton_pascal(N, K):
    K = min(K, N-K)
    T = [[1] * (K+1) for _ in range(N+1)]
    #T = []
    #for _ in range(N+1): T.append([1] * (K+1))
    for n in range(1, N+1):
        for k in range(1, min(K, n-1)+1):
            T[n][k] = T[n-1][k-1] + T[n-1][k]
    return T[N][K]

def newton_pascal_lomem(N, K):
    K = min(K, N-K)
    T = [1] * (K+1)
    for n in range(2, N+1):
        for k in range(min(K,n-1), 0, -1):
            T[k] = T[k-1] + T[k]
    return T[K]

print(newton_rec(190,87))
print(newton_iter(190,87))
print(newton_pascal(190,87))
print(newton_pascal_lomem(190,87))
