import pandas as pd
from levenshtein import *

def get_nearest_substrings(sector, minimum_distance = 1, number_of_substrings = 10, min_len_of_substrings = 4):
    companies_names = companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == sector]
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
    return sector_companies_df


technology_subs, technology_companies = get_nearest_substrings('technology', min_len_of_substrings = 6)
technology_subs
technology_companies

services_subs, services_companies = get_nearest_substrings('services', min_len_of_substrings = 6)
services_subs
services_companies


salMarkAdv_subs, salMarkAdv_companies = get_nearest_substrings('sales, marketing and advertising', min_len_of_substrings = 6)
salMarkAdv_subs
salMarkAdv_companies


primSec_subs, primSec_companies = get_nearest_substrings('primary sector', min_len_of_substrings = 5)
primSec_subs
primSec_companies

othConsRet_subs, othCosRet_companies = get_nearest_substrings('other consumer retail', min_len_of_substrings = 6)
othConsRet_subs
othCosRet_companies


onlPlatMark_subs, onlPlatMark_companies = get_nearest_substrings('online platforms and marketplaces', min_len_of_substrings = 5)
onlPlatMark_subs
onlPlatMark_companies

noProfGov_subs, noProfGov_companies = get_nearest_substrings('no-profit and government', min_len_of_substrings = 5)
noProfGov_subs
noProfGov_companies

industrial_subs, industrial_companies = get_nearest_substrings('industrial', min_len_of_substrings = 7)
industrial_subs
industrial_companies

foodBev_subs, foodBev_companies = get_nearest_substrings('food and beverage', min_len_of_substrings = 5)
foodBev_subs
foodBev_companies

evTravEnt_subs, evTravEnt_companies = get_nearest_substrings('events, travels, leisure and entertainment', min_len_of_substrings = 6)
evTravEnt_subs
evTravEnt_companies

education_subs, education_companies = get_nearest_substrings('education', min_len_of_substrings = 5)
education_subs
education_companies

consumElectr_subs, consumElectr_companies = get_nearest_substrings('consumer electronics', min_len_of_substrings = 7)
consumElectr_subs
consumElectr_companies

anPlanEnv_subs, anPlanEnv_companies = get_nearest_substrings('animals, plants and environment', min_len_of_substrings =5)
anPlanEnv_subs
anPlanEnv_companies

automotive_subs, automotive_companies = get_nearest_substrings('automotive', min_len_of_substrings = 5)
automotive_subs
automotive_companies

financials_subs, financials_companies = get_nearest_substrings('financials', min_len_of_substrings = 8)
financials_subs
financials_companies

healthcare_subs, healthcare_companies = get_nearest_substrings('healthcare', min_len_of_substrings = 6)
healthcare_subs
healthcare_companies
