# Scrapers

## Setup

All of the scrapers used in this repository uses the `selenium` with python and the `chromedriver` to scrape data from the websites. The extracted data is thn stored in either `csv` files or in a `mysql` database. The following are required to run these locally:

1. [Python](https://www.python.org/downloads/)

2. [Google Chrome](https://www.google.com/aclk?sa=l&ai=DChcSEwiMrfDZs6DrAhWb6-0KHX7zAZsYABABGgJkZw&sig=AOD64_3XDDyHtngcSeNZrOX6jAd1lkSQpg&q&adurl&ved=2ahUKEwig6-nZs6DrAhXwTxUIHdPRBKQQ0Qx6BAgoEAE)

3. [Chromedriver](https://chromedriver.chromium.org/downloads)

Make sure the version of chrome and chromedriver are in sync.

The `selenium` package can be installed by typing `pip3 install selenium` after installing python.

## Website's list
The following is the list of websites whose scraper can be found in this repository:

- [Amazon.com (Coupons)](https://www.amazon.com/Coupons/b/?ie=UTF8&node=2231352011&ref_=sv_subnav_goldbox_1)

- [Amazon.com (Top Deals)](https://www.amazon.com/gp/goldbox/ref=gbps_ftr_s-5_4e18_dls_UPCM?gb_f_deals1=enforcedCategories:2617941011%252C15684181%252C165796011%252C7147444011%252C3760911%252C283155%252C7147443011%252C502394%252C2335752011%252C541966%252C7586165011%252C172282%252C7141123011%252C1063306%252C7147442011%252C11260432011%252C172541%252C3760901%252C1055398%252C667846011%252C228013%252C16310091%252C284507%252C9479199011%252C2619525011%252C679255011%252C7192394011%252C6358539011%252C1040658%252C7147441011%252C11091801%252C1064954%252C2972638011%252C2619533011%252C328182011%252C3375251%252C165793011%252C679337011%252C6358543011%252C1040660%252C7147440011,dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CUPCOMING,dealTypes:DEAL_OF_THE_DAY%252CBEST_DEAL%252CLIGHTNING_DEAL,minRating:3,sortOrder:BY_SCORE,includedAccessTypes:GIVEAWAY_DEAL&pf_rd_p=4a0dd3f9-e36f-4203-83e5-3cbb64324e18&pf_rd_s=slot-5&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=Z90W0A6KYPBEPYFAXECH&ie=UTF8)

- [Amazon.com (Best Seller's)](https://www.amazon.com/Best-Sellers-Camera-Photo-Camcorders/zgbs/photo/172421/ref=zg_bs_nav_p_1_p)

- [Amazon.com (ISBN's)](amazon.com) & [Amazon.fr (ISBN's)](amazon.fr)

- [amhonline.amh.net.au (Medicine's data)](https://amhonline.amh.net.au/auth)

- [Aquaforestaquarium.com (Fishing appliances)](https://aquaforestaquarium.com/collections)

- [Bedetheque.com (Comic books)](https://www.bedetheque.com/bandes_dessinees_A.html)

- [boe.es (Education data)](https://www.boe.es/)

- [Namebio.com (Domain data)](https://namebio.com/)

- [Comicbookdb.com (Comic books)](http://comicbookdb.com/browse.php?search=Publisher&letter=A)

- [healthatlas.gov.gr (Doctor data)](https://healthatlas.gov.gr/HealthCare#!/)

- [Marinedepot.com (Fishing appliances)](https://www.marinedepot.com)

- [Midtowncomics.com (Comic books)](https://www.midtowncomics.com/store/search.asp?cat=62&scat=110&os=1&sh=100&reld=1/1/1900&reld2=1/1/1900&furl=cat=62@@scat=110@@pl=76)

- [PSX.com (Stock's data)](https://dps.psx.com.pk/historical)

- [thegreyhoundrecorder.com.au (Dog race data)](https://www.thegreyhoundrecorder.com.au/results/)

## End!