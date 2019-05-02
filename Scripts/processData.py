import pandas as pd
# pip install pandas

# the above r script used a url like below to generate the data
resultsLinki = 'https://www.waterqualitydata.us/Result/search?huc=170401&siteType=Lake, Reservoir, Impoundment;Stream&characteristicName=Temperature, water;Temperature, water, deg F;Calcium;pH&startDateLo=01-01-2009&mimeType=csv'
# the above should then be joined to the stations data below
sitesUrl = 'https://www.waterqualitydata.us/data/Station/search?huc=170401&mimeType=csv'

sitesFile = pd.read_csv(sitesUrl)
print(sitesFile.info())
