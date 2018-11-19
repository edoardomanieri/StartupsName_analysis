import pandas as pd
from levenshtein import *

def get_nearest_substrings(companies_df,sector, minimum_distance = 1, number_of_substrings = 5, min_len_of_substrings = 4):
    companies_names = companies_df['company_name'][companies_df['sector'] == sector]
    maximum = 0
    most_common_subs = []
    companies_subs = {}
    is_sorted = False
    for company in companies_names:
        for subs in find_all_substrings(str(company),min_len_of_substrings):
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
    companies_with_word = pd.Series(dic_companies_with_word)
    sector_companies = companies_df['company_name'][companies_df['sector'] == sector]
    dummies = [1 if company in companies_with_word[index_of_word] else 0 for company in sector_companies]
    sector_companies_df = pd.DataFrame(sector_companies)
    sector_companies_df[dummy_column_name] = pd.Series(dummies, index=sector_companies_df.index)
    return companies_df.merge(sector_companies_df, on='company_name')
