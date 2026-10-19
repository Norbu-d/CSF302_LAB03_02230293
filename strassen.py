# strassen.py
# Strassen's matrix multiplication (divide and conquer).
# Idea: split each n x n matrix into four n/2 x n/2 blocks. The normal method needs
# 8 block multiplications; Strassen computes the same result with only 7 (M1..M7),
# at the cost of extra additions/subtractions. Recurrence: T(n) = 7T(n/2) + O(n^2).

def add(A, B):
    # element-wise matrix addition
    return [[a + b for a, b in zip(r, s)] for r, s in zip(A, B)]

def sub(A, B):
    # element-wise matrix subtraction
    return [[a - b for a, b in zip(r, s)] for r, s in zip(A, B)]

def strassen(A, B, cnt):
    """Multiply A and B (n x n lists, n a power of 2).
    cnt is a dict {'mul': 0, 'add': 0} used to count scalar multiplications/additions."""
    n = len(A)
    # base case: 1x1 matrices -> a single scalar multiplication
    if n == 1:
        cnt['mul'] += 1
        return [[A[0][0] * B[0][0]]]
    h = n // 2
    # split A and B into four h x h quadrants each
    A11 = [r[:h] for r in A[:h]]; A12 = [r[h:] for r in A[:h]]
    A21 = [r[:h] for r in A[h:]]; A22 = [r[h:] for r in A[h:]]
    B11 = [r[:h] for r in B[:h]]; B12 = [r[h:] for r in B[:h]]
    B21 = [r[:h] for r in B[h:]]; B22 = [r[h:] for r in B[h:]]
    cnt['add'] += 18 * h * h  # 10 pre-additions + 8 post-additions of h x h blocks
    # the 7 recursive products (instead of 8)
    M1 = strassen(add(A11, A22), add(B11, B22), cnt)
    M2 = strassen(add(A21, A22), B11, cnt)
    M3 = strassen(A11, sub(B12, B22), cnt)
    M4 = strassen(A22, sub(B21, B11), cnt)
    M5 = strassen(add(A11, A12), B22, cnt)
    M6 = strassen(sub(A21, A11), add(B11, B12), cnt)
    M7 = strassen(sub(A12, A22), add(B21, B22), cnt)
    # combine M1..M7 into the four quadrants of the result
    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(add(sub(M1, M2), M3), M6)
    # stitch the quadrants back into one n x n matrix
    return [a + b for a, b in zip(C11, C12)] + [a + b for a, b in zip(C21, C22)]
