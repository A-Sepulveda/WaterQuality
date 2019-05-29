mapboxgl.accessToken = 'pk.eyJ1Ijoid3N1LWZwbSIsImEiOiJjanF5Mnpkd2ExbmxlM3htajh0cTRvNTE5In0.fVraCn9k7D9ncy49QtKXRQ';

function mapInits(){
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v8',
    center: [-110.748,43.299],
    zoom: 6.5
  });

  map.on('style.load', function () {
    map.addSource("markers", {
        "type": "geojson",
        "data": siteLocations
    });

    map.addLayer({
        "id": "sites",
        "interactive": true,
        "type": "circle",
        "source": "markers",
        "paint": {
          'circle-color': [
            'match',
            ['get', 'risk'],
            'veryHigh', '#f100e7',
            'high', '#f10000',
            'moderate', '#f7e600',
            'low', '#19e400',
            /* other */ '#7e7e7e'
            ],
            "circle-stroke-color":"#1d2a60",
            "circle-radius":6,
            "circle-stroke-width":0.5,
            "circle-color-transition": {
              "duration": 750,
              "delay": 0
            }
        }
    });

    map.on('mouseenter', 'sites', function(e) {
      // Change the cursor style as a UI indicator.
      map.getCanvas().style.cursor = 'pointer';
      jj=e.features[0].properties
    });

    map.on('click', 'sites', function(e) {
      // Change the cursor style as a UI indicator.
      console.log(e.features[0].properties.MonitoringLocationIdentifier)
      clickedSite=e.features[0].properties.MonitoringLocationIdentifier

    });

    map.on('mouseleave', 'sites', function() {
      map.getCanvas().style.cursor = '';
    });
  });
}

function filterRiskMapFeatures(){
  siteLocationsTemp={
    "type": "FeatureCollection",
    "features": []
  };
  siteLocations.features.forEach(function(thisSite){
    var tempSite=thisSite
    var siteId=tempSite.properties.MonitoringLocationIdentifier
    if(riskLookup[siteId]){
      tempSite.properties.risk=riskLookup[siteId]
    }else{
      tempSite.properties.risk='na'
    }
    siteLocationsTemp.features.push(tempSite)
  })
  updateSitesDateSource();
}

function updateSitesDateSource(){
  map.getSource('markers').setData(siteLocationsTemp);
  updateSelectedRiskSites()
}


function updateSelectedRiskSites(){
  filter=['all',['in','risk'].concat(selectedRiskValues)]
  map.setFilter('sites', filter)
}



// function filterMapFeatures(){
//   // checkdates
//   // var sitesFiltered=[]
//   //
//   // $.each(Object.keys(resultsData),function(i,thisSite){
//   //   if(new Date(resultsData[thisSite].minDate).getYear()+1900>=minYear){
//   //     sitesFiltered.push(thisSite)
//   //   }
//   // })
//   //
//   //
//   // filter=['all',['in','MonitoringLocationIdentifier'].concat(sitesFiltered)]
//
//   // var filteredSites=filterGeojson(sitesFiltered)
//
//   // map.fitBounds(turf.bbox(filteredSites),{
//   //   padding:20
//   // })
//   //
//   // map.setFilter('sites', filter)
// }
//
// function filterGeojson(sitesFiltered){
//   var filteredSites=siteLocations;
//   var newFeatures=[]
//   filteredSites.features.forEach(function(thisSite){
//     if(sitesFiltered.indexOf(thisSite.properties.MonitoringLocationIdentifier) > -1){
//       newFeatures.push(thisSite)
//     }
//   })
//   filteredSites.features=newFeatures
//   return(filteredSites)
// }
