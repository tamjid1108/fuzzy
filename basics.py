from collections import defaultdict

A = {
    2: 1,
    3: 0.4,
    1: 0.6,
    4: 0.2
}

B = {
    2: 0,
    3: 0.2,
    1: 0.2,
    4: 0.5
}


# union
def union(A, B):
    C = dict(A)
    for x in B.keys():
        if x in A.keys():
            C[x] = max(A[x], B[x])
        else:
            C[x] = B[x]
    return C


# intersection
def intersection(A, B):
    C = dict(A)
    for x in B.keys():
        if x in A.keys():
            C[x] = min(A[x], B[x])
        else:
            C[x] = B[x]
    return C


# complement
def complement(A):
    C = dict(A)
    for x in A.keys():
        C[x] = 1 - A[x]
    return C


# difference
def diff(A, B):
    return intersection(A, complement(B))


def verifyDeMorgans(A, B):
    if complement(union(A, B)) == intersection(complement(A), complement(B)) and complement(intersection(A, B)) == union(complement(A), complement(B)):
        return True
    else:
        return False


def cartesian(A, B):
    C = defaultdict(dict)
    for x in A.keys():
        for y in B.keys():
            C[x][y] = min(A[x], B[y])
    return dict(C)


def composition(R, S):
    C = defaultdict(dict)
    X = R.keys()
    Z = list(S.values())[0].keys()
    for x in R:
        for z in Z:
            C[x][z] = 0
            for y in R[x].keys():
                C[x][z] = max(C[x][z], min(R[x][y], S[y][z]))
    return dict(C)


print(union(A, B))
print(intersection(A, B))
print(complement(A))
print(diff(A, B))
if verifyDeMorgans(A, B):
    print("DeMorgans' law verified")


B = {
    5: 0,
    7: 0.2,
    6: 0.2,
    8: 0.8
}

C = {
    2: 0.5,
    3: 0.6,
    1: 0.1,
    4: 0.9
}

R = cartesian(A, B)
print(R)

S = cartesian(B, C)
print(S)

print(composition(R, S))
