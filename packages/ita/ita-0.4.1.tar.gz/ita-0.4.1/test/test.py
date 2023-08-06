# usage: pip install -e . && python test/test.py

import ita

print("version of ita:", ita.__version__)

def comb(n, m):
  if m == 0 or n == m:
    return 1
  else:
    return comb(n-1, m) + comb(n-1, m-1)

def total(x):
  c = 0
  for i in x:
    c = c + i
  return c

def count(x,k):
  # x = x + x
  # x = x * 3
  c = 0
  # import copy
  # x = copy.copy(x)
  # reversed(x)
  # c in x
  # print(x)
  # x.count(c)
  # min(x)
  # max(x)
  # len(x)
  # x.index(c)
  for i in x:
    c += 1
  return c


def sum_iter(arg):
  n = len(arg)
  if n == 0:
    return 0
  elif n == 1:
    return arg[0]
  else:
    c = n // 2
    return sum_iter(arg[:c]) + sum_iter(arg[c:])

def simple_sort(x):
  for i in range(len(x)):
    mi = i + x[i:].index(min(x[i:]))
    x[mi], x[i] = x[i], x[mi]

def mergesort(x):
    def merge(x, y):
        r = ita.array.make1d(len(x) + len(y))
        ix,iy = 0,0
        for i in range(0, len(r)):
            if iy >= len(y) or (ix < len(x) and x[ix] <= y[iy]):
                r[i] = x[ix]
                ix += 1
            else:
                r[i] = y[iy]
                iy += 1
        return r
    if len(x) <= 1:
        return x
    else:
        c = len(x) // 2
        return merge(mergesort(x[:c]), mergesort(x[c:]))

def bisection(data, key):
  s, t = 0, len(data)
  while t - s > 1:
    c = (s + t) // 2
    if data[c] == key:
      return c
    elif data[c] < key:
      s = c + 1
    else:
      t = c
  if data[s] == key:
    return s
  else:
    return -1

def kwaySort(x):
    def merge(x, y):
        r = ita.array.make1d(len(x) + len(y))
        ix,iy = 0,0
        for i in range(0, len(r)):
            if iy >= len(y) or (ix < len(x) and x[ix] <= y[iy]):
                r[i] = x[ix]
                ix += 1
            else:
                r[i] = y[iy]
                iy += 1
        return r
    if len(x) == 0:
      return x
    if len(x) == 1:
      return x[0]
    r = []
    for i in range(len(x) // 2):
      r.append(merge(x[2*i], x[2*i+1]))
    if len(x) % 2 == 1:
      r.append(x[-1])
    return kwaySort(r)

import sys
sys.setrecursionlimit(5000)

# x = ita.bench.toAccessCounting({1,2,3})
# print(x, type(x).__base__, 1 in x, list(x) * 3)
# x = ita.bench.toAccessCounting({1,2,3})

# data = [[[abs(i-j) ** 2 / 400 for j in range(20)]] for i in range(20)]
# ita.plot.animation_show(data, interval=1)

# print(ita.bench.evalWithTime((lambda x:x), complex(2,3)))

# x = ita.bench.toAccessCounting({1,2,3})
# print(x, isinstance(x, set))

# data = [[[i * 10 + j for i in range(10)] for j in range(k*5+5)] for k in range(10)]
# r = ita.bench.bench(kwaySort, data, criteria="access")
data = [ita.array.make2d(i+1,i+1) for i in range(10)]
r = ita.bench.bench(kwaySort, data, criteria="access")
data = [ita.array.make3d(i+1,i+1,2) for i in range(10)]
r = ita.bench.bench(kwaySort, data, criteria="access")
# ita.bench.plot(r)
# r = ita.bench.bench(kwaySort, data, criteria="recursion")
# ita.bench.plot(r)


print("count")
# r = ita.bench.bench(count, [(list(range(i*2+1)),i) for i in range(10)],
#                             criteria="access")
# # ita.bench.plot(r)
# r = ita.bench.bench(count, [(set(range(i*10)),i) for i in range(10)],
#                            criteria="access")
# r = ita.bench.bench(count, [(frozenset(range(i*500)),i) for i in range(10)],
#                              criteria="access")
# # ita.bench.plot(r)
# r = ita.bench.bench(count, [(dict((j,j) for j in range(i*500)),i)
#                             for i in range(10)],criteria="access")
# ita.bench.plot(r)
# r = ita.bench.bench(count, [(bytes((i*500)),i) for i in range(10)],
#                              criteria="access")
# # ita.bench.plot(r)
# r = ita.bench.bench(count, [(bytearray(j % 256 for j in range(i*500)),i) for i in range(10)], criteria="access")
# ita.bench.plot(r)
# r = ita.bench.bench(count, [(str(2**i), str(i)[0]) for i in range(10)],
#                             criteria="access")
# r = ita.bench.bench(count, [(range(500*i+1), i) for i in range(10)],
#                     criteria="access")
# ita.bench.plot(r)


# print("sum_iter")
# r = ita.bench.bench(sum_iter, [ita.array.make1d(i*500, random=True)
#                                for i in range(20)])
# ita.bench.plot(r)
# r = ita.bench.bench(sum_iter, [ita.array.make1d(i*500, random=True)
#                                for i in range(20)], criteria="access")
# ita.bench.plot(r)
# r = ita.bench.bench(sum_iter, [ita.array.make1d(i*500, random=True)
#                                for i in range(20)], criteria="recursion")
# ita.bench.plot(r)

# print("bisection")
# r = ita.bench.bench(bisection, [(range(10 ** i+1), 1) for i in range(5,15)],
#                     criteria="access")
# ita.bench.plot(r,xlogscale=True)


# print("comb")
# r = ita.bench.bench(comb, [(i*2+1,i) for i in range(10)])
# ita.bench.plot(r)
# r = ita.bench.bench(comb, [(i*2+1,i) for i in range(10)], criteria="recursion")
# ita.bench.plot(r)

# print("simple_sort")
# r = ita.bench.bench(simple_sort, [ita.array.make1d(i*50, random=True)
#                                   for i in range(20)], criteria="access")
# ita.bench.plot(r)

# print("merge_sort")
# r = ita.bench.bench(mergesort, [ita.array.make1d(i*500, random=True)
#                                 for i in range(20)], criteria="access")
# ita.bench.plot(r)

# import random
# data = [(2 * i + random.random()*10, 3 * i + random.random()*10) for i in range(100)]
# ita.plot.linear_fit(data)

