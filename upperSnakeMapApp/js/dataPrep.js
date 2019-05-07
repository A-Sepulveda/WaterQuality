var resultsData={}

function dataPrep(){
  $.each(results,function(i,obs){
    var thisLocationId=obs.siteId
    var thisDate=obs.date
    if(!resultsData[thisLocationId]){
      resultsData[thisLocationId]={
        pH:{},
        calcium:{},
        temperature:{}
      }
      resultsData[thisLocationId].pH[thisDate]=obs.phMean
      resultsData[thisLocationId].calcium[thisDate]=obs.caMean
      resultsData[thisLocationId].temperature[thisDate]=obs.tempMean
    }else{
      resultsData[thisLocationId].pH[thisDate]=obs.phMean
      resultsData[thisLocationId].calcium[thisDate]=obs.caMean
      resultsData[thisLocationId].temperature[thisDate]=obs.tempMean
    }
  })

  $.each(Object.keys(resultsData),function(i,thisSite){
    phDatesSorted=Object.keys(resultsData[thisSite].pH).sort(date_sort_desc)
    calciumDatesSorted=Object.keys(resultsData[thisSite].calcium).sort(date_sort_desc)
    temperatureDatesSorted=Object.keys(resultsData[thisSite].temperature).sort(date_sort_desc)
    resultsData[thisSite].pH.sortedDates=phDatesSorted
    resultsData[thisSite].calcium.sortedDates=calciumDatesSorted
    resultsData[thisSite].temperature.sortedDates=temperatureDatesSorted
  })

  addToMappedSites()
}

var date_sort_desc = function (date1, date2) {
  // This is a comparison function that will result in dates being sorted in
  // DESCENDING order.
  if (new Date(date1) > new Date(date2)) return -1;
  if (new Date(date1) < new Date(date2)) return 1;
  return 0;
};

function addToMappedSites(){
  $.each(siteLocations.features,function(i,thisSite){
    thisSiteId=thisSite.properties.MonitoringLocationIdentifier
    siteLocations.features[i].properties.pH=resultsData[thisSiteId].pH
    siteLocations.features[i].properties.calcium=resultsData[thisSiteId].calcium
    siteLocations.features[i].properties.temperature=resultsData[thisSiteId].temperature
  })
  // mapSites();
  mapInits();
}
