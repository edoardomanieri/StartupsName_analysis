*Healthcare, has medica
clear all
import delimited "/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/data/health_and_medica.csv", delimiter("|") 

*encoding country
encode country_code, gen(country)

*generating performance measure
gen perf_proxy = funding_total_usd - raised_amount_usd

*generating log of raised funds
gen log_raised = ln(raised_amount_usd)

*encoding market
encode market, gen(enc_mark)

*Regressions
xtset country
xtreg log_raised hasmedica i.enc_mark i.founded_year, fe cluster(country)  // no perf_proxy because endogenous --> multinomial logit 

encode status, gen(enc_status)
mlogit enc_status i.hasmedica, base(1) // base == acquired
margins hasmedica, atmeans predict(outcome(1))
margins hasmedica, atmeans predict(outcome(2))
margins hasmedica, atmeans predict(outcome(3))

tab status if hasmedica == 0
tab status if hasmedica == 1

 
**********************************************************************************
*Online-platforms, has .com
clear all
import delimited "/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/data/hasdotcom.csv", delimiter("|") 

*encoding country
encode country_code, gen(country)

*generating performance measure
gen perf_proxy = funding_total_usd - raised_amount_usd

*generating log of raised funds
gen log_raised = ln(raised_amount_usd)

*encoding market
encode market, gen(enc_mark)

*Regressions // no perf_proxy because endogenous --> multinomial logit 
xtset country
xtreg log_raised hasdotcom i.enc_mark i.founded_year if founded_year < 2008, fe cluster(country)   // no perf_proxy because endogenous --> multinomial logit 
xtreg log_raised hasdotcom i.enc_mark i.founded_year if founded_year < 2008 & founded_year > 2003, fe cluster(country) 
xtreg log_raised hasdotcom i.enc_mark i.founded_year if founded_year > 2008, fe cluster(country)


encode status, gen(enc_status)
mlogit enc_status i.hasdotcom, base(1) // base == acquired
margins hasdotcom, atmeans predict(outcome(1))
margins hasdotcom, atmeans predict(outcome(2))
margins hasdotcom, atmeans predict(outcome(3))

tab status if hasdotcom == 0
tab status if hasdotcom == 1

**********************************************************************************
*Technology, has algo-data-ai-deep-ytics
clear all
import delimited "/Users/lucamasserano/Desktop/BOCCONI/Business Analytics/Final project/Business_Analytics/data/final_tech_db.csv", delimiter("|") 

drop v1 
drop if company_name == ""

*encoding country
encode country_code, gen(enc_country)

*generating performance measure
gen perf_proxy = funding_total_usd - raised_amount_usd

*generating log of raised funds
gen log_raised = ln(raised_amount_usd)

*encoding market
encode market, gen(enc_mark)

*generating a dummy which contains all the others
gen has_all = hasai | hasalgo | hasdata | hasdeep | hasytics

*Regressions
xtset enc_country
xtreg log_raised has_all i.enc_mark i.founded_year, fe cluster(enc_country) // without perf_proxy because endogenous --> multinomial logit

encode status, gen(enc_status)
mlogit enc_status i.has_all, base(1) // base == acquired
margins has_all, atmeans predict(outcome(1))
margins has_all, atmeans predict(outcome(2))
margins has_all, atmeans predict(outcome(3))

tab status if has_all == 0
tab status if has_all == 1

