import pandas as pd

cd '/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/code'

data_dir = "/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/data"

companies_data = pd.read_excel(data_dir + '/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Companies")
rounds_data = pd.read_excel(data_dir + '/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Rounds")
ba_sheet = pd.read_excel(data_dir + '/categories.xlsx').rename({"Market": "market", "Sector" : "sector"}, axis = "columns")
companies_data = companies_data[pd.notnull(companies_data['name'])]
companies_data = companies_data[companies_data['founded_year'] >= 1990]

companies_data.rename({'name': 'company_name'}, axis = "columns", inplace = True)
companies_rounds = companies_data.merge(rounds_data, on="company_name")
companies_rounds = companies_rounds[companies_rounds['funding_round_type'] == 'seed']
companies_rounds.count()
companies_rounds = companies_rounds[companies_rounds['raised_amount_usd'] != 0]
companies_rounds = companies_rounds[pd.notnull(companies_rounds['raised_amount_usd'])]
companies_rounds.count()

companies_rounds = companies_rounds[["company_name", "market", "funding_total_usd", "status", "country_code", "city", "funding_rounds", "founded_year", "raised_amount_usd"]]
companies_rounds_sector = companies_rounds.merge(ba_sheet, on="market")
companies_rounds_sector = companies_rounds_sector[pd.notnull(companies_rounds_sector['market'])]
companies_rounds_sector.count()
companies_grouped = companies_rounds_sector.groupby(["company_name"])[['company_name', 'raised_amount_usd']].sum()
companies_rounds_sector = companies_grouped.merge(companies_rounds_sector, on=["company_name", "raised_amount_usd"])
companies_rounds_sector.groupby('sector').count()

def is_online_platform(company_name):
    return str(company_name).__contains__(".com") or str(company_name).__contains__(".it")\
            or str(company_name).__contains__(".org")\
            or str(company_name).__contains__(".net")

mask = [is_online_platform(name) for name in companies_rounds_sector['company_name']]
companies_rounds_sector_onl = companies_rounds_sector[mask]
companies_rounds_sector.loc[companies_rounds_sector['company_name'].isin(companies_rounds_sector_onl['company_name']), 'sector'] = 'online platforms and marketplaces'

companies_rounds_sector.to_csv(data_dir + "/final_data.csv", sep="|", encoding="UTF-8")
