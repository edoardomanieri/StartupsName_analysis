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

rename hasmedica medical

*Regressions
xtset country
xtreg log_raised medical i.enc_mark i.founded_year, fe cluster(country)  // no perf_proxy because endogenous --> multinomial logit
est store a
esttab a using results.tex,b se stats(r2) star(* 0.1 ** 0.05 *** 0.01) mtitles("medical") title("healthcare") keep(medical _cons) replace

encode status, gen(enc_status)
mlogit enc_status i.medical, base(1) // base == acquired
margins medical, atmeans predict(outcome(1)) post
est store m1
mlogit enc_status i.medical, base(1)
margins medical, atmeans predict(outcome(2)) post
est store m2
mlogit enc_status i.medical, base(1)
margins medical, atmeans predict(outcome(3)) post
est store m3

esttab m1 m2 m3 using results.tex,b se star(* 0.1 ** 0.05 *** 0.01) mtitles("acquired" "closed" "operating") title("healthcare performance control") append

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

rename hasdotcom dotcom

*Regressions // no perf_proxy because endogenous --> multinomial logit
xtset country
xtreg log_raised dotcom i.enc_mark i.founded_year if founded_year >= 2008, fe cluster(country)
estimates store a
coefplot a, bylabel(After 2008) ||, keep(*:dotcom) xscale(range (-3 3)) xlabel(-3 "-3" -2 "-2" 0 "0" 1 "1" 2 "2" 3 "3")  xline(0, lcolor( black) lwidth(thin) lpattern(dash)) ciopts(recast(rcap))
xtreg log_raised dotcom i.enc_mark i.founded_year if founded_year < 2008, fe cluster(country)   // no perf_proxy because endogenous --> multinomial logit
estimates store b
coefplot b, bylabel(Before 2008) ||, keep(*:dotcom) xscale(range (-3 3)) xlabel(-3 "-3" -2 "-2" 0 "0" 1 "1" 2 "2" 3 "3")  xline(0, lcolor( black) lwidth(thin) lpattern(dash)) ciopts(recast(rcap))
xtreg log_raised dotcom i.enc_mark i.founded_year if founded_year < 2008 & founded_year > 2002, fe cluster(country)
estimates store c
esttab a b c using results.tex,b se stats(r2) star(* 0.1 ** 0.05 *** 0.01) mtitles("after 2007" "before 2008" "between 2003 and 2007") title("online platforms") keep(dotcom _cons) append
coefplot c, bylabel(Between 2003 and 2007) ||, keep(*:dotcom) xscale(range (-3 3)) xlabel(-3 "-3" -2 "-2" 0 "0" 1 "1" 2 "2" 3 "3")  xline(0, lcolor( black) lwidth(thin) lpattern(dash)) ciopts(recast(rcap))


coefplot a, bylabel(After 2008) || b, bylabel(Between 2003 and 2008) || c, bylabel(before 2008) ||, keep(*:hasdotcom)


encode status, gen(enc_status)
mlogit enc_status i.dotcom, base(1) // base == acquired
margins dotcom, atmeans predict(outcome(1)) post
est store m1
mlogit enc_status i.dotcom, base(1)
margins dotcom, atmeans predict(outcome(2)) post
est store m2
mlogit enc_status i.dotcom, base(1)
margins dotcom, atmeans predict(outcome(3)) post
est store m3

esttab m1 m2 m3 using results.tex,b se star(* 0.1 ** 0.05 *** 0.01) mtitles("acquired" "closed" "operating") title("online platforms performance control") append


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
gen trending_name = hasai | hasalgo | hasdata | hasdeep | hasytics


*Regressions
xtset enc_country
xtreg log_raised trending_name i.enc_mark i.founded_year, fe cluster(enc_country) // without perf_proxy because endogenous --> multinomial logit
estimates store a
esttab a using results.tex,b se stats(r2) star(* 0.1 ** 0.05 *** 0.01) mtitles("trending name") title("technology") keep(trending_name _cons) append

encode status, gen(enc_status)
mlogit enc_status i.trending_name, base(1) // base == acquired
margins trending_name, atmeans predict(outcome(1)) post
est store m1
mlogit enc_status i.trending_name, base(1)
margins trending_name, atmeans predict(outcome(2)) post
est store m2
mlogit enc_status i.trending_name, base(1)
margins trending_name, atmeans predict(outcome(3)) post
est store m3

esttab m1 m2 m3 using results.tex,b se star(* 0.1 ** 0.05 *** 0.01) mtitles("acquired" "closed" "operating") title("technology performance control") append
