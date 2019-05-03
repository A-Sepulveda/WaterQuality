packs <- c('readr', 'tidyverse', 'dataRetrieval', 'reshape2', 'scales', 'stringr',
           'leaflet', 'knitr', 'lubridate')
lapply(packs, require, character.only = T)

startDate <- as.Date("2009-01-01")
analytes <- c("Temperature, water", "Temperature, water, deg F","Calcium", "pH")
siteTypes <- c("Lake, Reservoir, Impoundment","Stream")
hucToGet <- c("140401","140402") #this is the upper snake

# using the parameters above this returns 2760 obersvations
upperSnakeTenYears = readWQPdata(huc = hucToGet,
  siteType = siteTypes,
  characteristicName=analytes,
  startDateLo=startDate)

atts<-attributes(upperSnakeTenYears)


# the above query via the readWQPdata function is just generating the link below on the backend.. this can be obtained from the attributes of the upperSnakeTenYears DF
'https://www.waterqualitydata.us/Result/search?huc=170401&siteType=Lake, Reservoir, Impoundment;Stream&characteristicName=Temperature, water;Temperature, water, deg F;Calcium;pH&startDateLo=01-01-2009&mimeType=csv'


# below are a couple other urls that had some userful information
# userful UI for testing parameters, queries etc
'https://www.waterqualitydata.us/data/swagger-ui.html'

# this seems to pull just upper snake stations and not observations
"https://www.waterqualitydata.us/data/Station/search?huc=170401&startDateLo=01-01-2019&mimeType=csv"

# this seems to provide a list of all the available characteristic names in json
'https://www.waterqualitydata.us/services/codes/characteristicname?mimeType=json'
