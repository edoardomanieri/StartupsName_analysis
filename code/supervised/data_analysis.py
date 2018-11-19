import pandas as pd
from levenshtein import *

cd '/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/code'

data_dir = "/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/data"

companies_rounds_sector = pd.read_csv(data_dir + "/final_data.csv", sep='|')
companies_rounds_sector = companies_rounds_sector.iloc[:,1:]
companies_rounds_sector["company_name"][companies_rounds_sector["sector"] == "technology"]


##############################

## SUPERVISED ##

##############################

trends = ["ai", "data", "ytics", "deep", "algo", "ify"]

descr_keywords = ["ai", "artificial intelligence", "data", "deep learning", "algorithm", "algorithms", "machine learning", "analytics",
                    "data mining", "internet of things", "iot"]

trend_subs, trend_companies = get_nearest_substrings("healthcare", number_of_substrings = 10, min_len_of_substrings = 4)

hasData = append_dummy_column(companies_rounds_sector, trend_companies, 2, "technology", "hasData")
hasIfy = append_dummy_column(companies_rounds_sector, trend_companies, 4, "technology", "hasIfy")
hasYtics = append_dummy_column(companies_rounds_sector, trend_companies, 5, "technology", "hasYtics")

hasData_Ify_Ytics = hasData.merge(hasIfy).merge(hasYtics)

hasData_Ify_Ytics.to_csv(data_dir + "/hasData_Ify_Ytics.csv", sep="|", encoding="UTF-8")
