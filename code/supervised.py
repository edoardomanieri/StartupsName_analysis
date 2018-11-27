import pandas as pd
import ctypes

#### to compile the c file ---> cc -fPIC -shared -o liblev.so levenshtein.c

## instructions that allow to use the levenshtein functions in the file levesthein.c
_lev = ctypes.CDLL('./liblev.so')
_lev.levenshtein.argtypes = (ctypes.c_char_p, ctypes.c_char_p)
_lev.levenshtein.restypes = ctypes.c_uint

def find_all_substrings(string, min_number_of_letters):
    """Short summary.

    Parameters
    ----------
    string : string
        string to substring.
    min_number_of_letters : int
        minimum number of letter.

    Returns
    -------
    list
        list of substrings.

    """
    res = []
    for i in range(min_number_of_letters, len(string)):
        res += substrings(string, i)
    return res

def substrings(string, number_of_letters):
    """Short summary.

    Parameters
    ----------
    string : string
        string to substring.
    number_of_letters : type
        number of letter of substrings.

    Returns
    -------
    list
        list of substrings.
    """
    res = []
    if len(string) < number_of_letters:
        res.append(string)
        return res
    for i in range(len(string) - number_of_letters + 1):
        res.append(string[i: i + number_of_letters])
    return res

def levenshtein_max(company_names, substring, param):
    """Short summary.

    Parameters
    ----------
    company_names : list
        list of company names.
    substring : string
        substring to find.
    param : int
        minimum distance accepted by the algorithm.

    Returns
    -------
    int
        number of substring with respected distance.
    list
        list of companies with respected distance.
    """
    res = 0
    common_companies = []
    substring = str(substring)
    c_substring = substring.encode('utf-8')
    for comp in company_names:
        comp_temp = str(comp)[:]
        comp_temp = comp_temp.lower()
        for comp_subs in substrings(comp_temp, len(substring)):
            c_comp_subs = comp_subs.encode('utf-8')
            dist = _lev.levenshtein(c_comp_subs, c_substring)
            if dist <= param:
                res += 1
                common_companies.append(comp)
    return res, common_companies

def get_nearest_substrings(dataframe, sector, minimum_distance = 0, number_of_substrings = 10, min_len_of_substrings = 4):
    """Short summary.

    Parameters
    ----------
    dataframe : pandas DataFrame
        dataframe with companies.
    sector : string
        sector to analize.
    minimum_distance : int
        minimum levesthein distance accepted.
    number_of_substrings : int
        number of substrings returned.
    min_len_of_substrings : int
        minimum length of substrings.

    Returns
    -------
    list
        list of firsts n substrings that respected the distance the greatest number of times.
    list
        list of ompanies where the n substrings come from.
    """
    trends = ["ai", "data", "ytics", "deep", "algo", "ify"]
    companies_names = dataframe['company_name'][dataframe['sector'] == sector]
    most_common_subs = []
    companies_subs = {}
    is_sorted = False
    for subs in trends:
        subs = subs.lower()
        result, temp = levenshtein_max(list(companies_names), subs, minimum_distance)
        if len(most_common_subs) < number_of_substrings and (subs, result) not in most_common_subs:
            most_common_subs.append((subs, result))
            companies_subs[subs] = temp
        if len(most_common_subs) == number_of_substrings:
            if not is_sorted:
                most_common_subs.sort(key=lambda tup: tup[1], reverse=True)
                is_sorted = True
            if result > most_common_subs[-1][1] and (subs, result) not in most_common_subs:
                companies_subs.pop(most_common_subs[-1][0])
                companies_subs[subs] = temp
                most_common_subs[-1] = (subs, result)
                most_common_subs.sort(key=lambda tup: tup[1], reverse=True)
    return most_common_subs, companies_subs

def append_dummy_column(companies_df, dic_companies_with_word, index_of_word, sector, dummy_column_name):
    """Short summary.

    Parameters
    ----------
    companies_df : pandas DataFrame
        dataframe target.
    dic_companies_with_word : dict
        dictionary to find out for what word append the corrispondent dummy column.
    index_of_word : int
        index of the word in the dictionary.
    sector : string
        sector to analyze.
    dummy_column_name : string
        name of the dummy variable column in the new DataFrame.

    Returns
    -------
    pandas DataFrame
        DataFrame with the corrispondent dummy column appended.

    """
    companies_with_word = pd.Series(dic_companies_with_word)
    sector_companies = companies_df['company_name'][companies_df['sector'] == sector]
    dummies = [1 if company in companies_with_word[index_of_word] else 0 for company in sector_companies]
    sector_companies_df = pd.DataFrame(sector_companies)
    sector_companies_df[dummy_column_name] = pd.Series(dummies, index=sector_companies_df.index)
    return companies_df.merge(sector_companies_df, on='company_name')


def companies_keywords(dataframe, descr_keywords):
    """Short summary.

    Parameters
    ----------
    dataframe : pandas DataFrame
        dataframe with descriptions to analyze.
    descr_keywords : string
        keywords to be searched in the descriptions.

    Returns
    -------
    list
        list of companies with at least a keyword in the description.

    """
    companies = []
    for index, descr in enumerate(dataframe["description"]):
        for word in descr.split():
            word = word.lower()
            if word in descr_keywords:
                companies.append( dataframe[["company_name"]].iloc[index,:] )
                break
    return companies
