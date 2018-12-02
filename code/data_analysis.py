import pandas as pd
import numpy as np
import supervised as sv
import unsupervised as usv

# datasets loading

# name dataset loading
companies_rounds_sector = pd.read_csv("../data/datasets_cleaned/initial_dataset_cleaned.csv", sep='|')
companies_rounds_sector = companies_rounds_sector.iloc[:,1:]

# descripions dataset loading
final = pd.read_csv("../data/datasets_cleaned/technology_companies_with_descriptions.csv", sep='|')

################################# TECHNOLOGY ################################################

# name words
trends = ["ai", "data", "ytics", "deep", "algo", "ify"]

#description words
descr_keywords = ["ai", "artificial intelligence", "data", "deep learning", "algorithm", "algorithms", "machine learning", "analytics",
                    "data mining", "internet of things", "iot"]

# find companies that have keywords
count_comp, companies_descr = len(sv.companies_keywords(final, descr_keywords)), sv.companies_keywords(final, descr_keywords)
companies_descriptions = pd.DataFrame(data = companies_descr)

# insert into dataset Trendalytics and Vantage Analytics
final_tech_data = companies_descriptions.merge(final)
temp = companies_rounds_sector[companies_rounds_sector["company_name"].isin(["Trendalytics", "Vantage Analytics"])].iloc[:,:]
temp["description"] = pd.Series([np.nan, np.nan], index = temp.index)
final_tech_data = pd.concat( (final_tech_data, temp) )

# find out which companies have keywords in their name
trend_subs, trend_companies = sv.get_nearest_substrings(final, "technology", number_of_substrings = 10, min_len_of_substrings = 4)
trend_companies = { "ai":["Tempo AI", "Wit.ai", "aiHit", "Feedzai", "Aivo"], "deep":["DeepField"], "data":trend_companies["data"], "algo":trend_companies["algo"], "ytics":trend_companies["ytics"] + ["Trendalytics", "Vantage Analytics"] }
trend_companies

# append dummy column for analysis with stata
hasAI = sv.append_dummy_column(final_tech_data, trend_companies, 0, "technology", "hasAI")
hasAlgo = sv.append_dummy_column(final_tech_data, trend_companies, 1, "technology", "hasAlgo")
hasData = sv.append_dummy_column(final_tech_data, trend_companies, 2, "technology", "hasData")
hasDeep = sv.append_dummy_column(final_tech_data, trend_companies, 3, "technology", "hasDeep")
hasYtics = sv.append_dummy_column(final_tech_data, trend_companies, 4, "technology", "hasYtics")
final_tech_data = hasAI.merge(hasAlgo).merge(hasData).merge(hasDeep).merge(hasYtics)
final_tech_data = final_tech_data[pd.notnull(final_tech_data["company_name"])]

##################################### HEALTHCARE ################################################

# find out which companies have the mosts near substrings in their name
healthcare_subs, healthcare_companies = usv.get_nearest_substrings(companies_rounds_sector, 'healthcare', minimum_distance = 1, min_len_of_substrings = 6, number_of_substrings = 10)

# append dummy column for analysis with stata
hasMedica = usv.append_dummy_column(companies_rounds_sector, healthcare_companies, 3, "healthcare", 'hasMedica')



#################################### ONLINE PLATFORMS ############################################

# find out which companies have the mosts near substrings in their name
onlPlatMark_subs, onlPlatMark_companies = usv.get_nearest_substrings(companies_rounds_sector,'online platforms and marketplaces', min_len_of_substrings = 5, number_of_substrings = 10)

# append dummy column for analysis with stata
hasdotcom = usv.append_dummy_column(companies_rounds_sector, onlPlatMark_companies, 0, "online platforms and marketplaces", 'hasDotCom')


#save files
final_tech_data.to_csv("../data/datasets_processed/technology_dataset.csv", sep="|", encoding="UTF-8")
hasMedica.to_csv("../data/datasets_processed/healthcare_dataset.csv", sep="|", encoding="UTF-8")
hasdotcom.to_csv("../data/datasets_processed/onlinePlatforms_dataset.csv", sep="|", encoding="UTF-8")
