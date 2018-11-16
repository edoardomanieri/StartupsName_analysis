import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from levenshtein import *

cd '/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/code'

data_dir = "/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/data"

companies_data = pd.read_excel(data_dir + '/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Companies")
rounds_data = pd.read_excel(data_dir + '/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Rounds")
ba_sheet = pd.read_excel(data_dir + '/categories.xlsx').rename({"Market": "market", "Sector" : "sector"}, axis = "columns")
companies_data = companies_data[pd.notnull(companies_data['name'])]
companies_data = companies_data[companies_data['founded_year'] >= 1990]

companies_data.rename({'name': 'company_name'}, axis = "columns", inplace = True)
companies_rounds = companies_data.merge(rounds_data, on="company_name", how="left")
companies_rounds = companies_rounds[companies_rounds['funding_round_type'] == 'seed']
companies_rounds.count()
companies_rounds = companies_rounds[companies_rounds['raised_amount_usd'] != 0]
companies_rounds = companies_rounds[pd.notnull(companies_rounds['raised_amount_usd'])]
companies_rounds.count()

companies_rounds = companies_rounds[["company_name", "market", "funding_total_usd", "status", "country_code", "city", "funding_rounds", "founded_year", "raised_amount_usd"]]
companies_rounds_sector = companies_rounds.merge(ba_sheet, on="market", how="left")
companies_rounds_sector = companies_rounds_sector[pd.notnull(companies_rounds_sector['market'])]
companies_rounds_sector.count()
companies_grouped = companies_rounds_sector.groupby(["company_name"])[['company_name', 'raised_amount_usd']].sum()
companies_rounds_sector = companies_grouped.merge(companies_rounds_sector, on=["company_name", "raised_amount_usd"], how="left")
companies_rounds_sector.groupby('sector').count()

companies_rounds_sector.to_csv("./final_data.csv", sep="|", encoding="UTF-8")



companies_rounds_sector = pd.read_csv(data_dir + "/final_data.csv", sep='|')
companies_rounds_sector = companies_rounds_sector.iloc[:,1:]
companies_rounds_sector



companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'healthcare']


def get_nearest_substrings(sector, minimum_distance = 1, number_of_substrings = 5, min_len_of_substrings = 4):
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

s, c = get_nearest_substrings('healthcare', min_len_of_substrings = 5)
