import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from levenshtein import *


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

companies_rounds_sector.to_csv("./final_data.csv", sep="|", encoding="UTF-8")



companies_rounds_sector = pd.read_csv("./final_data.csv", sep='|')
companies_rounds_sector = companies_rounds_sector.iloc[:,1:]
companies_rounds_sector



companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'financials']

param = 1
maximum = 0
max_sub = None
company_sub = None
for company in companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'financials']:
    for subs in substrings(str(company),5):
        lev = levenshtein_max(list(companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'financials']), subs, param)
        if lev > maximum:
            maximum = lev
            max_sub = subs
            company_sub = company
max_sub
levenshtein_max(list(companies_rounds_sector['company_name'][companies_rounds_sector['sector'] == 'financials']), max_sub, param)
