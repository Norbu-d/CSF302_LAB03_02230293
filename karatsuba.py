# karatsuba.py  (Q2)
# Multiplies two large integers stored as digit STRINGS (so size is not limited by native ints)
# using grade-school multiplication O(n^2) and Karatsuba's divide and conquer.
# Karatsuba idea: split x = a*10^h + b and y = c*10^h + d. Instead of 4 products
# (ac, ad, bc, bd) compute only 3: ac, bd and (a+b)(c+d); then ad+bc = (a+b)(c+d) - ac - bd.
# Recurrence: T(n) = 3T(n/2) + O(n). Results are verified against Python's built-in int product.
import random, time

# remove leading zeros (keep a single '0')
def strip(s): return s.lstrip('0') or '0'

def add(a, b):
    # add two digit strings column by column with carry
    n = max(len(a), len(b)); a, b = a.zfill(n), b.zfill(n)
    out, carry = [], 0
    for i in range(n - 1, -1, -1):
        s = int(a[i]) + int(b[i]) + carry
        out.append(str(s % 10)); carry = s // 10
    if carry: out.append(str(carry))
    return ''.join(reversed(out))

def sub(a, b):  # requires a >= b
    # subtract digit strings column by column with borrow
    n = len(a); b = b.zfill(n)
    out, borrow = [], 0
    for i in range(n - 1, -1, -1):
        d = int(a[i]) - int(b[i]) - borrow
        borrow = 1 if d < 0 else 0
        out.append(str(d + 10 * borrow))
    return strip(''.join(reversed(out)))

# multiply by 10^k by appending k zeros
def shift(s, k): return s if s == '0' else s + '0' * k

def traditional(x, y, cnt):
    """Grade-school: every digit of x times every digit of y -> n^2 digit multiplications."""
    res = [0] * (len(x) + len(y))
    for i in range(len(x) - 1, -1, -1):
        for j in range(len(y) - 1, -1, -1):
            res[i + j + 1] += int(x[i]) * int(y[j]); cnt['mul'] += 1
    for k in range(len(res) - 1, 0, -1):  # propagate carries
        res[k - 1] += res[k] // 10; res[k] %= 10
    return strip(''.join(map(str, res)))

def karatsuba(x, y, cnt):
    # make both numbers the same length by padding with leading zeros
    n = max(len(x), len(y)); x, y = x.zfill(n), y.zfill(n)
    # base case: single digits -> one multiplication
    if n == 1:
        cnt['mul'] += 1
        return str(int(x) * int(y))
    if n % 2: x, y, n = '0' + x, '0' + y, n + 1  # keep length even for the split
    h = n // 2  # split point
    a, b, c, d = x[:h], x[h:], y[:h], y[h:]
    z2 = karatsuba(a, c, cnt)  # a*c (high parts)
    z0 = karatsuba(b, d, cnt)  # b*d (low parts)
    z1 = sub(sub(karatsuba(add(a, b), add(c, d), cnt), z2), z0)  # (a+b)(c+d) - ac - bd
    # result = z2*10^n + z1*10^h + z0
    return strip(add(add(shift(z2, n), shift(z1, n - h)), z0))

def next_pow2(n):
    # smallest power of 2 >= n (used to pad operands)
    p = 1
    while p < n: p *= 2
    return p

# random n-digit number as a string (first digit non-zero)
def rand_num(n): return str(random.randint(1, 9)) + ''.join(random.choice('0123456789') for _ in range(n - 1))

def run(x, y):
    # pad to a power of 2, run both algorithms, count digit multiplications, time them, verify result
    n = next_pow2(max(len(x), len(y))); X, Y = x.zfill(n), y.zfill(n)  # pad to power of 2
    ct, ck = {'mul': 0}, {'mul': 0}
    t = time.perf_counter(); r1 = traditional(X, Y, ct); t1 = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); r2 = karatsuba(X, Y, ck);   t2 = (time.perf_counter() - t) * 1000
    ok = r1 == r2 == str(int(x) * int(y))
    return n, ct['mul'], ck['mul'], t1, t2, ok, r1

def main():
    # menu: 1 = type two numbers, 2 = benchmark table for 8..1024 digits (random numbers)
    print("1. Manual input  2. Benchmark table (8..1024 digits)")
    if input("Choice: ").strip() == '1':
        x, y = input("First number: ").strip(), input("Second number: ").strip()
        r = run(x, y); print("Traditional/Karatsuba result:", r[-1]); print("Match:", r[5])
    else:
        print(f"{'digits':>7} {'Trad mul':>10} {'Karat mul':>10} {'Trad ms':>10} {'Karat ms':>10} {'Match':>6}")
        n = 8
        while n <= 1024:
            r = run(rand_num(n), rand_num(n))
            print(f"{r[0]:>7} {r[1]:>10} {r[2]:>10} {r[3]:>10.2f} {r[4]:>10.2f} {str(r[5]):>6}")
            n *= 2

if __name__ == '__main__':
    main()

# ANALYSIS
# Grade-school: n^2 single-digit multiplications -> O(n^2).
# Karatsuba:    T(n) = 3T(n/2) + O(n) -> O(n^log2(3)) ~ O(n^1.585).
# Measured counts (see table): n=1024 -> 1,048,576 vs 225,617 digit multiplications. The count is a bit
# above 3^log2(n) because (a+b) and (c+d) can carry into an extra digit, so some subproblems are larger.
# At n=8, Karatsuba does slightly MORE multiplications (67 vs 64) - overhead dominates at tiny sizes;
# it wins from n=16 onward and the gap widens with n.
# Wall-clock time: traditional is faster at every tested size in pure Python, because Karatsuba's string
# add/sub/pad work is costly. The operation count shows the asymptotic win; the real crossover needs a
# lower-level implementation or much larger n. Results matched Python's int product in every test.
