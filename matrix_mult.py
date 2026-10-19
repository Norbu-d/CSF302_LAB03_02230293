# matrix_mult.py  (Q1)
# Multiplies two n x n matrices (n = power of 2) with the traditional O(n^3) method and
# with Strassen's algorithm (strassen.py), shows both results, verifies they match,
# and compares multiplication counts and running time.
import random, time
from strassen import strassen

def traditional(A, B, cnt):
    # triple nested loop: C[i][j] = sum over k of A[i][k] * B[k][j]  -> n^3 multiplications
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = 0
            for k in range(n):
                s += A[i][k] * B[k][j]
                cnt['mul'] += 1
            C[i][j] = s
    return C

# generate an n x n matrix of random digits 0-9
def rand_matrix(n): return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]

def show(M, name):
    # print a matrix row by row with aligned columns
    print(name)
    for r in M: print(' '.join(f'{x:6}' for x in r))

def run(A, B, display=True):
    # run both algorithms on A, B; time them, count multiplications, check results are equal
    n = len(A)
    ct, cs = {'mul': 0, 'add': 0}, {'mul': 0, 'add': 0}
    t = time.perf_counter(); C1 = traditional(A, B, ct); t1 = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); C2 = strassen(A, B, cs);    t2 = (time.perf_counter() - t) * 1000
    if display:
        show(C1, 'Traditional result:'); show(C2, "Strassen result:")
    return n, ct['mul'], cs['mul'], cs['add'], t1, t2, C1 == C2

def main():
    # menu: 1 = type matrices in, 2 = random matrices of chosen n, 3 = benchmark table for n = 2..128
    print("1. Manual input  2. Random (single n)  3. Benchmark table (n = 2..128)")
    ch = input("Choice: ").strip()
    if ch == '1':
        n = int(input("n (power of 2): "))
        assert n & (n - 1) == 0 and n > 0, "n must be a power of 2"
        print("Enter matrix A rows:"); A = [list(map(int, input().split())) for _ in range(n)]
        print("Enter matrix B rows:"); B = [list(map(int, input().split())) for _ in range(n)]
        r = run(A, B); print("Results match:", r[-1])
    elif ch == '2':
        n = int(input("n (power of 2): "))
        assert n & (n - 1) == 0 and n > 0, "n must be a power of 2"
        A, B = rand_matrix(n), rand_matrix(n)
        show(A, 'A:'); show(B, 'B:')
        r = run(A, B, display=n <= 16); print("Results match:", r[-1])
    else:
        print(f"{'n':>4} {'Trad mul':>10} {'Strassen mul':>13} {'Strassen add':>13} {'Trad ms':>10} {'Strassen ms':>12} {'Match':>6}")
        n = 2
        while n <= 128:
            r = run(rand_matrix(n), rand_matrix(n), display=False)
            print(f"{r[0]:>4} {r[1]:>10} {r[2]:>13} {r[3]:>13} {r[4]:>10.2f} {r[5]:>12.2f} {str(r[6]):>6}")
            n *= 2

if __name__ == '__main__':
    main()

# ANALYSIS
# Traditional: T(n) = n^3 multiplications -> O(n^3).
# Strassen:    T(n) = 7T(n/2) + O(n^2) -> O(n^log2(7)) ~ O(n^2.81); multiplications = 7^log2(n).
# The table shows the multiplication gap widening with n (n=128: 823,543 vs 2,097,152).
# Wall-clock time: Strassen is slower here (n=128: ~2105 ms vs ~160 ms). With a 1x1 base case it does
# 18 matrix additions per level plus list slicing/copying, which costs far more than the multiplications
# saved at these sizes. Practical versions switch to the traditional method below a cutoff (~64-128+).
# Both methods produced identical matrices in every test (Match = True).
