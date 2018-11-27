import pandas as pd

# to determine if a company is an online platform
def is_online_platform(company_name):
    return str(company_name).__contains__(".com") or str(company_name).__contains__(".it")\
            or str(company_name).__contains__(".org")\
            or str(company_name).__contains__(".net")

# companies datasets loading
companies_data = pd.read_excel('../data/initial_datasets/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Companies")
rounds_data = pd.read_excel('../data/initial_datasets/crunchbase_monthly_export_d43b4klo2ade53.xlsx', sheet_name= "Rounds")
ba_sheet = pd.read_excel('../data/initial_datasets/categories.xlsx').rename({"Market": "market", "Sector" : "sector"}, axis = "columns")


# companies dataset cleaning process
companies_data = companies_data[pd.notnull(companies_data['name'])]
companies_data = companies_data[companies_data['founded_year'] >= 1990]
companies_data.rename({'name': 'company_name'}, axis = "columns", inplace = True)
companies_rounds = companies_data.merge(rounds_data, on="company_name")
companies_rounds = companies_rounds[companies_rounds['funding_round_type'] == 'seed']
companies_rounds = companies_rounds[companies_rounds['raised_amount_usd'] != 0]
companies_rounds = companies_rounds[pd.notnull(companies_rounds['raised_amount_usd'])]
companies_rounds = companies_rounds[["company_name", "market", "funding_total_usd", "status", "country_code", "city", "funding_rounds", "founded_year", "raised_amount_usd"]]
companies_rounds_sector = companies_rounds.merge(ba_sheet, on="market")
companies_rounds_sector = companies_rounds_sector[pd.notnull(companies_rounds_sector['market'])]
companies_grouped = companies_rounds_sector.groupby(["company_name"])[['company_name', 'raised_amount_usd']].sum()
companies_rounds_sector = companies_grouped.merge(companies_rounds_sector, on=["company_name", "raised_amount_usd"])
mask = [is_online_platform(name) for name in companies_rounds_sector['company_name']]
companies_rounds_sector_onl = companies_rounds_sector[mask]
companies_rounds_sector.loc[companies_rounds_sector['company_name'].isin(companies_rounds_sector_onl['company_name']), 'sector'] = 'online platforms and marketplaces'

# description dataset loading
descr1 = pd.read_csv("../data/initial_datasets/descriptions_scraped/Descriptions.csv", sep = "|")
descr2 = pd.read_csv("../data/initial_datasets/descriptions_scraped/Descriptions1.csv", sep = "|")
descr3 = pd.read_csv("../data/initial_datasets/descriptions_scraped/Descriptions_tech_pericoli.csv", sep = "|")
descr4 = pd.read_csv("../data/initial_datasets/descriptions_scraped/technology_desc.csv", sep = "|").iloc[:,1:]

# description dataset cleaning process
technology_descriptions = pd.concat( (descr1, descr2, descr3, descr4) )
technology_descriptions.drop_duplicates(inplace = True)
technology_descriptions = technology_descriptions[technology_descriptions["company_name"] != "company_name"]
technology_descriptions = technology_descriptions[technology_descriptions["company_name"] != "Company"]
technology_descriptions_final = companies_rounds_sector.merge(technology_descriptions)

# save files
companies_rounds_sector.to_csv("../data/datasets_cleaned/initial_dataset_cleaned.csv", sep="|", encoding="UTF-8")
technology_descriptions_final.to_csv("../data/datasets_cleaned/technology_companies_with_descriptions.csv", sep="|", encoding="UTF-8")
