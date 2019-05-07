python
import pandas as pd
# pip install pandas
# -----------------------------------
# -----------------------------------
# -----------------------------------
#  importing sites and results
# -----------------------------------
# -----------------------------------
# -----------------------------------
# the above r script used a url like below to generate the data
resultsUrl = 'https://www.waterqualitydata.us/Result/search?huc=140401&siteType=Lake%2C%20Reservoir%2C%20Impoundment%3BStream&characteristicName=Temperature%2C%20water%3BTemperature%2C%20water%2C%20deg%20F%3BCalcium%3BpH&startDateLo=01-01-2009&zip=no&sorted=no&mimeType=tsv'
# the above should then be joined to the stations data below
sitesUrl = 'https://www.waterqualitydata.us/data/Station/search?huc=170401&mimeType=csv'
# this reads in csv from sites and results from either the url (dynamic) or via the local file
# sitesFile = pd.read_csv(sitesUrl)
sitesFile = pd.read_csv('./sampleData/170401_sites_fromDf.csv')
# resultsFile = pd.read_csv(resultsUrl)
# resultsFile = pd.read_csv('./sampleData/170401_since_01012009.csv')
# I added 8 rows of nas, whitespace for testing to the below
resultsFile = pd.read_csv('./sampleData/170401_since_01012009.csv')
print(resultsFile.info())
print(sitesFile.info())

# -----------------------------------
# -----------------------------------
# -----------------------------------
#  CLEANING IMPORTED DATA
# -----------------------------------
# -----------------------------------
# -----------------------------------
# these are teh columns we'd like to subset from the results data
resultsDataColumns=["OrganizationFormalName","ActivityStartDate", "ActivityStartTime.Time", "ActivityStartTime.TimeZoneCode","CharacteristicName",
         "MonitoringLocationIdentifier","SampleCollectionMethod.MethodName", "SampleCollectionEquipmentName","ResultMeasureValue", "ResultMeasure.MeasureUnitCode",
         "ResultSampleFractionText","ResultAnalyticalMethod.MethodName", "MethodDescriptionText","ProviderName"]
# this subsets the results data by just selecting the above columns
resultsFile=resultsFile[resultsDataColumns]
print(resultsFile.info())
# -----------------------------------
# DROP NA ROWS
# -----------------------------------
# drop those rows that have na values in ResultMeasureValue
print(len(resultsFile))
resultsFile=resultsFile.dropna(subset=['ResultMeasureValue'])
print(len(resultsFile))
# -----------------------------------
# -----------------------------------
# REMOVE WHITE space
# -----------------------------------
# -----------------------------------
lastRow=len(resultsFile)
# this looks like white space was already stripped on import
print(resultsFile.iloc[lastRow-10:lastRow,9])
# let's force some white space on that obs and then change it
# resultsFile.iloc[lastRow-1:lastRow,9]='               dec C                 '
whiteSpaceExample=resultsFile.iloc[lastRow-1:lastRow,9]
print(whiteSpaceExample)
print(whiteSpaceExample.str.strip())
# or on the whole column
print(resultsFile.iloc[lastRow-10:lastRow,9].str.strip())
# or modify the whole column and remove white space permanently
resultsFile.iloc[0:lastRow,9]=resultsFile.iloc[0:lastRow,9].str.strip()
print(resultsFile.iloc[0:lastRow,9])
# -----------------------------------
# -----------------------------------
# CALCIUM specific cleaning
# -----------------------------------
# -----------------------------------
sampleFractionFilter=['Dissolved','Total']
# this is just for testing
# subset of calcium rows
calciumRows=resultsFile.loc[resultsFile['CharacteristicName'] == 'Calcium']
# 1527 rows have calcium
len(calciumRows)
# this removes those rows that don't have a ResultSampleFractionText value in sampleFractionFilter
calciumRowsFiltered=calciumRows[calciumRows.ResultSampleFractionText.isin(sampleFractionFilter)]
# 1504 rows
len(calciumRowsFiltered)
# now apply to entire dataframe
# these are the ~23 rows to drop
resultsFile.loc[(resultsFile['CharacteristicName'] == 'Calcium') & (~resultsFile.ResultSampleFractionText.isin(sampleFractionFilter))]
# or the n-23 calcium rows not to drop... note the ~
resultsFile.loc[(resultsFile['CharacteristicName'] == 'Calcium') & (resultsFile.ResultSampleFractionText.isin(sampleFractionFilter))]
# drop them from the entire DF with drop and not index
resultsFile=resultsFile.drop(resultsFile[(resultsFile['CharacteristicName'] == 'Calcium') & (~resultsFile.ResultSampleFractionText.isin(sampleFractionFilter))].index)
# now we only want those calcium values that were measured in either micrograms per liter (ug/l) and milligrams per liter (mg/l)
# i added three rows to the dirty file with values of foo in the measurement units
# also added 3 rows where I converted mg/l to ug/l since there were no instances of ug/l in this query result
#
# first let's only grab those rows with mg and ug values.. this will drop the 3x foo values
measureUnitCodeFilter=['ug/l','mg/l']
# again... these are the 3 rows with foo to remove
resultsFile.loc[(resultsFile['CharacteristicName'] == 'Calcium') & (~resultsFile["ResultMeasure.MeasureUnitCode"].isin(measureUnitCodeFilter))]
# drop them from the data frame
resultsFile=resultsFile.drop(resultsFile[(resultsFile['CharacteristicName'] == 'Calcium') & (~resultsFile["ResultMeasure.MeasureUnitCode"].isin(measureUnitCodeFilter))].index)
# ---
# convert ug/l values to mg/l
# which rows are ug/l
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l',['ResultMeasure.MeasureUnitCode','ResultMeasureValue']]
# just the measurement values
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l','ResultMeasureValue']
# divided by 1000
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l','ResultMeasureValue']/1000
# convert those in the dataframe
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l','ResultMeasureValue']=resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l','ResultMeasureValue']/1000
# and change the units
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l','ResultMeasure.MeasureUnitCode']
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'ug/l','ResultMeasure.MeasureUnitCode']='mg/l'
# -----------------------------------
# -----------------------------------
# TEMPERATURE SPECIFIC CLEANING
# really just converting those values in F to C
# -----------------------------------
# -----------------------------------
# which rows are in F
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'deg F']
# and their values
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'deg F','ResultMeasureValue']
# convert those to c
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'deg F','ResultMeasureValue']=(resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'deg F','ResultMeasureValue']-32)/1.8
# and change the units
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'deg F','ResultMeasure.MeasureUnitCode']='deg C'
#also make sure all those rows have a Characteristic Name of tmperature units are labeled as temp
resultsFile.loc[resultsFile['ResultMeasure.MeasureUnitCode'] == 'deg C','CharacteristicName']='temperature'

# -----------------------------------
# -----------------------------------
# PH SPECIFIC CLEANING ------NEED TO DO THIS NEXT
# -----------------------------------
# -----------------------------------
phRows=resultsFile.loc[resultsFile['CharacteristicName'] == 'pH']
# remove any rows with values outsite 0-14
# which rows are those? its the 56 below
resultsFile.loc[(resultsFile['CharacteristicName'] == 'pH') & (resultsFile.ResultMeasureValue>14) | (resultsFile.ResultMeasureValue<0),'ResultMeasureValue']
# drop them from the df
resultsFile=resultsFile.drop(resultsFile[(resultsFile['CharacteristicName'] == 'pH') & (resultsFile.ResultMeasureValue>14) | (resultsFile.ResultMeasureValue<0)].index)
# -----------------------------------
# -----------------------------------
# ORGANIZE BY ROW WHERE EACH ROW IS A UNIQUE DATE AT A UNIQUE MonitoringLocationIdentifier
# -----------------------------------
# -----------------------------------
# create a temporary vector of site id and date.. this will be used to assess unique place times
resultsFile["siteTimes"]=resultsFile.ActivityStartDate+'_break_'+resultsFile.MonitoringLocationIdentifier
uniqueSiteDates=resultsFile.siteTimes.unique()
#
newColumns=['siteId','date','phMean','phMax','phMin','phSd','phCnt','caMean','caMax','caMin','caSd','caCnt','tempMean','tempMax','tempMin','tempSd','tempCnt','uniqueSiteDates']
# create the empty df
newDf=pd.DataFrame(columns=newColumns)
newDf.uniqueSiteDates=uniqueSiteDates
newDf.info()

theseDates=newDf['uniqueSiteDates'].str.split('_break_',expand=True)[0]
theseSites=newDf['uniqueSiteDates'].str.split('_break_',expand=True)[1]

newDf["date"]=theseDates
newDf["siteId"]=theseSites

# iterative over unique days at each unique site
for siteDate in uniqueSiteDates:
    # these are the rows for this site on this day
    theseSiteDateRows=resultsFile.loc[resultsFile.siteTimes==siteDate]
    # and the total obersvations
    totalObs=len(theseSiteDateRows)
    thisSiteDateStats=theseSiteDateRows[["ResultMeasureValue","CharacteristicName"]].groupby("CharacteristicName").describe()
    thisSiteDateStats=thisSiteDateStats.ResultMeasureValue
    thisSiteDateStats['CharacteristicName']=thisSiteDateStats.index
    thisSiteDateStats.CharacteristicName
    if thisSiteDateStats.CharacteristicName.str.contains('pH').sum()>0:
        thisSubDat=thisSiteDateStats.loc[thisSiteDateStats.CharacteristicName=='pH']
        newDf.loc[newDf.uniqueSiteDates==siteDate,'phMean']=float(thisSubDat['mean'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'phMax']=float(thisSubDat['max'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'phMin']=float(thisSubDat['min'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'phSd']=float(thisSubDat['std'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'phCnt']=float(thisSubDat['count'])
    if thisSiteDateStats.CharacteristicName.str.contains('Calcium').sum()>0:
        thisSubDat=thisSiteDateStats.loc[thisSiteDateStats.CharacteristicName=='Calcium']
        newDf.loc[newDf.uniqueSiteDates==siteDate,'caMean']=float(thisSubDat['mean'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'caMax']=float(thisSubDat['max'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'caMin']=float(thisSubDat['min'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'caSd']=float(thisSubDat['std'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'caCnt']=float(thisSubDat['count'])
    if thisSiteDateStats.CharacteristicName.str.contains('temperature').sum()>0:
        thisSubDat=thisSiteDateStats.loc[thisSiteDateStats.CharacteristicName=='temperature']
        newDf.loc[newDf.uniqueSiteDates==siteDate,'tempMean']=float(thisSubDat['mean'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'tempMax']=float(thisSubDat['max'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'tempMin']=float(thisSubDat['min'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'tempSd']=float(thisSubDat['std'])
        newDf.loc[newDf.uniqueSiteDates==siteDate,'tempCnt']=float(thisSubDat['count'])

# drop the unique site date column afterwards
newDf.drop(['uniqueSiteDates'],axis=1)
# write it all to a new CSV
resultsFile.to_csv('./sampleData/170401_since_01012009_cleaned.csv', sep=',', encoding='utf-8', index=False)
# -----------------------------------
# -----------------------------------
# -----------------------------------
#  CLEAN THE SITES A BIT
# -----------------------------------
# -----------------------------------
# -----------------------------------
sitesDataColumns=["OrganizationIdentifier","OrganizationFormalName", "MonitoringLocationTypeName", "MonitoringLocationIdentifier", "MonitoringLocationName","LatitudeMeasure","LongitudeMeasure"]
sitesFile=sitesFile[sitesDataColumns]
siteTypeFilter=["Stream","River/Stream","Lake, Reservoir, Impoundment"]
sitesFile[sitesFile.MonitoringLocationTypeName.isin(siteTypeFilter)]
# this subsets the results data by just selecting the above columns
sitesFile=sitesFile[sitesFile.MonitoringLocationTypeName.isin(siteTypeFilter)]
# for now, let's drop any sites that don't have obersvations
uniqueResultSites=resultsFile.MonitoringLocationIdentifier.unique()
sitesFile=sitesFile[sitesFile.MonitoringLocationIdentifier.isin(uniqueResultSites)]

sitesFile.to_csv('./sampleData/170401_sites_cleaned.csv', sep=',', index=False)
