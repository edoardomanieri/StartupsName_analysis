import pandas as pd
from helper_functions import *

companies_rounds_sector = pd.read_csv("./final_data.csv", sep='|')
companies_rounds_sector = companies_rounds_sector.iloc[:,1:]

s, c = get_nearest_substrings(companies_rounds_sector, 'healthcare', minimum_distance = 1, min_len_of_substrings = 6, number_of_substrings = 10)

hasHealth = append_dummy_column(companies_rounds_sector, c, 0, "healthcare", 'hasHealth')
hasMedica = append_dummy_column(companies_rounds_sector, c, 3, "healthcare", 'hasMedica')
health_and_medica = hasHealth.merge(hasMedica)
health_and_medica.to_csv("./health_and_medica.csv", sep="|", encoding="UTF-8")

onlPlatMark_subs, onlPlatMark_companies = get_nearest_substrings(companies_rounds_sector,'online platforms and marketplaces', min_len_of_substrings = 5, number_of_substrings = 10)
hasdotcom = append_dummy_column(companies_rounds_sector, onlPlatMark_companies, 0, "online platforms and marketplaces", 'hasDotCom')
hasdotcom.to_csv("./hasdotcom.csv", sep="|", encoding="UTF-8")

financials_subs, financials_companies = get_nearest_substrings(companies_rounds_sector,'financials', min_len_of_substrings = 8, number_of_substrings = 10)
hasProperty = append_dummy_column(companies_rounds_sector, financials_companies, 8, "financials", 'hasProperty')
hasPayments = append_dummy_column(companies_rounds_sector, financials_companies, 9, "financials", 'hasPayments')
hasSolutions = append_dummy_column(companies_rounds_sector, financials_companies, 3, "financials", 'hasSolutions')
property_payments_solutions = hasPayments.merge(hasProperty).merge(hasSolutions)
property_payments_solutions.to_csv("./property_payments_solutions.csv", sep="|", encoding="UTF-8")

technology_subs, technology_companies = get_nearest_substrings(companies_rounds_sector,'technology', min_len_of_substrings = 6, number_of_substrings = 10)

services_subs, services_companies = get_nearest_substrings('services', min_len_of_substrings = 6, number_of_substrings = 10)

salMarkAdv_subs, salMarkAdv_companies = get_nearest_substrings('sales, marketing and advertising', min_len_of_substrings = 6, number_of_substrings = 10)

industrial_subs, industrial_companies = get_nearest_substrings('industrial', min_len_of_substrings = 7, number_of_substrings = 10)

evTravEnt_subs, evTravEnt_companies = get_nearest_substrings('events, travels, leisure and entertainment', min_len_of_substrings = 6, number_of_substrings = 10)
