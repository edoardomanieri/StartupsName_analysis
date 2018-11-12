import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from levesthein import *

direc = "/home/edoardo/Desktop/Business"

companies_data = pd.read_excel(direc + '/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Companies")
rounds_data = pd.read_excel(direc + '/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Rounds")
ba_sheet = pd.read_excel( direc + '/BA-project.xlsx').rename({"Market": "market", "Sector" : "sector"}, axis = "columns")
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

min = np.inf
min_sub = None
company_sub = None
for company in companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'services']:
    for subs in find_all_substring(str(company), 5):
        lev = levenshtein_sum(companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'services'], subs)
        if lev < min:
            min = lev
            min_sub = subs
            company_sub = company
min_sub
company_sub


companies_rounds_sector['company_name'][1500:1504]
