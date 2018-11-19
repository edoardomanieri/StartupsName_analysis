import ctypes

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
