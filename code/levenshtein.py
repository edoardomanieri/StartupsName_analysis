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

#cd '/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/code'

#### to compile the c file ---> cc -fPIC -shared -o liblev.so levenshtein.c

_lev = ctypes.CDLL('./liblev.so')
_lev.levenshtein.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
_lev.levenshtein.restypes = ctypes.c_uint

def find_all_substrings(string, min_number_of_letters):
    res = []
    for i in range(min_number_of_letters, len(string)):
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

def levenshtein_max(company_names, substring, param):
    res = 0
    common_companies = []
    substring = str(substring)
    c_substring = substring.encode('utf-8')
    for comp in company_names:
        for elem in comp.split():
            elem = str(elem)
            c_elem = elem.encode('utf-8')
            dist = _lev.levenshtein(c_elem, c_substring)
            if len(c_elem) > len(c_substring):
                dist -= len(c_elem) - len(c_substring)
            if dist <= param:
                res += 1
                common_companies.append(comp)
    return res, common_companies
