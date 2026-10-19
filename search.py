# search.py  (Q3)
# Menu-driven program: generate a sorted random array, search it with Binary Search
# (split in 2) and Ternary Search (split in 3), and record step/frequency counts
# (number of key comparisons) for best case, worst case and increasing n.
# Counting rule: every key-vs-element comparison (== or <) counts as 1 step.
import random, math

def binary_search(arr, key):
    # returns (index or -1, comparison count). Halves the range each step using the middle element.
    lo, hi, c = 0, len(arr) - 1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        c += 1
        if arr[mid] == key: return mid, c
        c += 1
        if key < arr[mid]: hi = mid - 1
        else: lo = mid + 1
    return -1, c

def ternary_search(arr, key):
    # returns (index or -1, comparison count). Two probes m1, m2 split the range into 3 parts.
    lo, hi, c = 0, len(arr) - 1, 0
    while lo <= hi:
        third = (hi - lo) // 3  # size of one third of the current range
        m1, m2 = lo + third, hi - third
        c += 1
        if arr[m1] == key: return m1, c
        c += 1
        if arr[m2] == key: return m2, c
        c += 1
        if key < arr[m1]: hi = m1 - 1
        else:
            c += 1
            if key > arr[m2]: lo = m2 + 1
            else: lo, hi = m1 + 1, m2 - 1
    return -1, c

# n unique random integers, sorted ascending
def gen(n): return sorted(random.sample(range(1, 10 * n + 1), n))

# keys that sit exactly on the first probe of each algorithm -> best case (1 comparison)
def best_keys(arr):  # first probe of each algorithm hits the key
    n = len(arr); third = (n - 1) // 3
    return arr[(n - 1) // 2], arr[third]

def table():
    # option 7: best/worst comparison counts for increasing n, next to log2(n) and log3(n)
    print(f"{'n':>9} {'Bin best':>9} {'Ter best':>9} {'Bin worst':>10} {'Ter worst':>10} {'log2 n':>8} {'log3 n':>8}")
    for n in [10, 100, 1000, 10**4, 10**5, 10**6]:
        a = gen(n); kb, kt = best_keys(a); absent = a[-1] + 1
        print(f"{n:>9} {binary_search(a, kb)[1]:>9} {ternary_search(a, kt)[1]:>9} "
              f"{binary_search(a, absent)[1]:>10} {ternary_search(a, absent)[1]:>10} "
              f"{math.log2(n):>8.2f} {math.log(n, 3):>8.2f}")

def main():
    # menu loop; arr holds the current sorted array (empty until option 1 is used)
    arr = []
    while True:
        print("\n1. Generate sorted array  2. Display array  3. Binary search  4. Ternary search")
        print("5. Best case counts  6. Worst case counts  7. Comparison table  0. Exit")
        ch = input("Choice: ").strip()
        if ch == '0': break
        if ch == '1':
            arr = gen(int(input("n: "))); print("Array generated.")
        elif ch == '7': table()
        elif not arr: print("Generate an array first (option 1).")
        elif ch == '2': print(arr)
        elif ch in ('3', '4'):
            key = int(input("Key: "))
            idx, c = (binary_search if ch == '3' else ternary_search)(arr, key)
            print(f"Found at index {idx}" if idx >= 0 else "Not found", f"| comparisons = {c}")
        elif ch == '5':
            kb, kt = best_keys(arr)
            print(f"Binary  best (key={kb}): {binary_search(arr, kb)[1]} comparison(s)")
            print(f"Ternary best (key={kt}): {ternary_search(arr, kt)[1]} comparison(s)")
        elif ch == '6':
            absent = arr[-1] + 1  # larger than all -> search goes to the end
            print(f"Binary  worst (key={absent} absent): {binary_search(arr, absent)[1]} comparisons")
            print(f"Ternary worst (key={absent} absent): {ternary_search(arr, absent)[1]} comparisons")

if __name__ == '__main__':
    main()

# ANALYSIS
# Binary:  T(n) = T(n/2) + O(1) -> log2(n) levels, up to 2 comparisons per level -> ~2*log2(n).
# Ternary: T(n) = T(n/3) + O(1) -> log3(n) levels, up to 4 comparisons per level -> ~4*log3(n)
#          = (4/log2(3)) * log2(n) ~ 2.52 * log2(n).
# Both are O(log n). Ternary has fewer levels but does more comparisons per level, so in the worst case
# it makes ~26% more comparisons than binary (n=10^6: 52 vs 40). Best case is 1 comparison for both
# (key at the first probe). Binary search is therefore the better choice.
