import ctypes
# def call_counter(func):
#     def helper(*args, **kwargs):
#         helper.calls += 1
#         return func(*args, **kwargs)
#     helper.calls = 0
#     helper.__name__= func.__name__
#     return helper
# memo = {}
# @call_counter
# def levenshtein(s, t):
#     if s == "":
#         return len(t)
#     if t == "":
#         return len(s)
#     cost = 0 if s[-1] == t[-1] else 1
#
#     i1 = (s[:-1], t)
#     if not i1 in memo:
#         memo[i1] = levenshtein(*i1)
#     i2 = (s, t[:-1])
#     if not i2 in memo:
#         memo[i2] = levenshtein(*i2)
#     i3 = (s[:-1], t[:-1])
#     if not i3 in memo:
#         memo[i3] = levenshtein(*i3)
#     res = min([memo[i1]+1, memo[i2]+1, memo[i3]+cost])

#    return res


_lev = ctypes.CDLL('./liblev.so')
_lev.levenshtein.argtypes = (ctypes.POINTER(ctypes.c_char), ctypes.POINTER(ctypes.c_char))

def find_all_substring(string, n ):
    res = []
    for i in range(n, len(string)):
        res += substrings(string, i)
    return res

def substrings(string, number_of_letters):
    res = []
    if len(string) < number_of_letters:
        res.append(string)
        return res
    for i in range(len(string) - number_of_letters + 1):
        res.append(string[i: i + number_of_letters])
    return res

def levenshtein_max(list_of_strings, substring):
    res = 0
    array_type_sub = ctypes.c_char * len(substring)
    substring = str(substring)
    for elem in list_of_strings:
        elem = str(elem)
        array_type_elem = ctypes.c_char * len(elem)
        if _lev.levenshtein(array_type_elem(*elem), array_type_sub(*substring)) < 3:
            res += 1
    return res
