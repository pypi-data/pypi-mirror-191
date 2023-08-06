from matplotlib import pyplot
import time
import types
import collections
import copy

import ita.global_vars as ig

def argToStr(arg):
    def argToStrMain(arg):
        if isinstance(arg, tuple) and len(arg) > 3:
            return "(" + argToStrMain(arg[0]) + ", " + argToStrMain(arg[1]) + " ...)"
        if isinstance(arg, list) and len(arg) > 3:
            return "[" + argToStrMain(arg[0]) + ", " + argToStrMain(arg[1]) + " ...]"
            pass
        if (isinstance(arg, set) or
            isinstance(arg, frozenset)) and len(arg) > 3:
            s = "{"
            c = 0
            for i in arg:
                s += argToStrMain(i)
                c += 1
                if c >= 2:
                    break
                s += ", "
            return s + "...}"
        if isinstance(arg, dict) and len(arg) > 3:
            s = "{"
            c = 0
            for k in arg.keys():
                s += str(k) + ":" + argToStrMain(arg[k])
                c += 1
                if c >= 2:
                    break
                s += ", "
            return s + "...}"
        if isinstance(arg, str):
            s = "'" + arg + "'"
        else:
            s = str(arg)
        if len(s) > 15:
            return s[:15] + "..." + s[-1]
        else:
            return s
    if isinstance(arg, tuple):
        return "(" + ", ".join(map(argToStrMain, arg)) + ")"
    else:
        return "(" + argToStrMain(arg) + ")"

def default_measure(x):
    if isinstance(x, tuple):
        return sum(default_measure(y) for y in x)
    if hasattr(type(x), "__len__"):
        return len(x)
    if hasattr(type(x), "__abs__"):
        return abs(x)
    raise TypeError("bench: the size of the argument is unknown. Specify the mesure.")

def count_recursive_call(func):
   def wrapper(*args, **kwargs):
       ig._recursion_cnt += 1
       return func(*args, **kwargs)
   return wrapper

def evalWithTime(f, arg, criteria="time", measure=default_measure, count=1):
    if not hasattr(f, '__call__'):
        raise TypeError("evalWithTime: first argument must be a function")
    if criteria == "time":
        func = f
    elif criteria == "access":
        ig._data_access_cnt = 0
        arg = toAccessCounting(arg)
        func = f
    elif criteria == "recursion":
        ig._recursion_cnt = 0
        tempf = copy.deepcopy(f)
        func = count_recursive_call(tempf)
        tempf.__globals__[f.__name__] = func
    else:
        raise TypeError("evalWithTime: unsupported criteria")
    
    print("evaluating ", f.__name__ + argToStr(arg), "... ", end="")
    start = time.perf_counter()
    for i in range(count):
        if isinstance(arg, tuple):
            func(*arg)
        else:
            func(arg)
    et = (time.perf_counter() - start)
    print("finished in ", et, " seconds.")
    
    if criteria == "time":
        return (measure(arg), et / count)
    elif criteria == "access":
        return (measure(arg), ig._data_access_cnt / count)
    elif criteria == "recursion":
        tempf.__globals__[f.__name__] = f
        return (measure(arg), ig._recursion_cnt / count)
    else:
        raise TypeError("evalWithTime: unsupported criteria")


def bench(f, args, criteria="time", measure=default_measure, count=1):
    if not hasattr(f, '__call__'):
        raise TypeError("bench: first argument must be a function")
    if not isinstance(args, collections.abc.Sequence):
        raise TypeError("bench: second argument must be a series of arguments")
    x, y = [], []
    for arg in args:
        v, w = evalWithTime(f, arg,
                            criteria=criteria, measure=measure, count=count)
        x.append(v)
        y.append(w)
    return (x, y)

def plot(d, xlogscale=False, ylogscale=False):
    if xlogscale:
        pyplot.xscale("log")
    else:
        pyplot.xscale("linear")
    if ylogscale:
        pyplot.yscale("log")
    else:
        pyplot.yscale("linear")
    pyplot.plot(d[0],d[1])
    pyplot.show()


import ita.global_vars as ig

import types

def accessCountingData(orig):
    t = type(orig)
    if t == range:
        return AccessCountingRange(orig)
    cn = "AccessCounting" + t.__name__
    # nc = types.new_class(cn, (t,))
    nc = type(cn, (t,), {})
    def _getitem(self, idx):
        ig._data_access_cnt += 1
        if isinstance(idx, slice):
            return nc(super(nc,self).__getitem__(idx))
        else:
            return super(nc,self).__getitem__(idx)
    def _setitem(self, key, value):
        ig._data_access_cnt += 1
        return super(nc,self).__setitem__(key, value)
    def _iter(self):
        return AccessCountIterator(super(nc,self).__iter__())
    def _add(self, arg):
        return nc(super(nc,self).__add__(arg))
    def _mul(self, arg):
        return nc(super(nc,self).__mul__(arg))
    def _copy(self, *arg):
        return nc(super(nc,self).__copy__(*arg))
    def _str(self, *arg):
        s = super(nc,self).__str__(*arg)
        h, sep, t = s.partition(cn)
        if h == '':
            return t[1:-1] if len(t) > 2 else "{}"
        return s
    atlist = [('__getitem__', _getitem),
              ('__setitem__', _setitem),
              ('__iter__', _iter),
              ('__add__', _add),
              ('__mul__', _mul),
              ('__copy__', _copy),
              ('__str__', _str)]
    for an, f in atlist:
        if hasattr(t, an):
            setattr(nc, an, f)
    return nc(orig)

class AccessCountingRange(collections.abc.Sequence):
    def __init__(self, orig):
        self.ran = orig
        self.start = orig.start
        self.stop = orig.stop
        self.step = orig.step
        pass
    def __getitem__(self, idx):
        ig._data_access_cnt += 1
        if isinstance(idx, slice):
            return AccessCountingRange(self.ran[idx])
        else:
            return self.ran[idx]
    def __iter__(self):
        return AccessCountIterator(self.ran.__iter__())
    def __copy__(self):
        return AccessCountingRange(self.ran)
    def __str__(self):
        return str(self.ran)
    def __len__(self):
        return len(self.ran)
    def __min__(self):
        ig._data_access_cnt += 1
        return min(self.ran)
    def __max__(self):
        ig._data_access_cnt += 1
        return max(self.ran)
    def __contains__(self, key):
        ig._data_access_cnt += 1
        return (key in self.ran)
    def __reversed__(self):
        return AccessCountIterator(reversed(self.ran))
    def index(self, *args):
        ig._data_access_cnt += 1
        return self.ran.index(*args)
    def count(self, key):
        ig._data_access_cnt += 1
        return self.ran.count(key)

class AccessCountIterator(collections.abc.Iterator):
   def __init__(self, it, *args):
       self._it = it
   def __iter__(self):
       return self
   def __next__(self):
       ig._data_access_cnt += 1
       return self._it.__next__()

def toAccessCounting(d):
    # supported: range, str, dict, list, set, frozenset, tuple, ...
    if (isinstance(d, range) or isinstance(d, str) or isinstance(d, bytes)
        or isinstance(d, bytearray)):
        return accessCountingData(d)
    if isinstance(d, dict):
        return accessCountingData(type(d)((k, toAccessCounting(v))
                                          for k,v in d.items()))
    if isinstance(d, list) or isinstance(d, set) or isinstance(d, frozenset):
        return accessCountingData(type(d)(toAccessCounting(v) for v in d))
    if isinstance(d, tuple):
        return type(d)(toAccessCounting(v) for v in d)
    return d



