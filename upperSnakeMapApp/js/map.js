mapboxgl.accessToken = 'pk.eyJ1Ijoid3N1LWZwbSIsImEiOiJjanF5Mnpkd2ExbmxlM3htajh0cTRvNTE5In0.fVraCn9k7D9ncy49QtKXRQ';

function mapInits(){
  map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v8',
    center: [-110.748,43.299],
    zoom: 7.5
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
            "circle-color":"#606dc9",
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

    map.on('mouseleave', 'sites', function() {
      map.getCanvas().style.cursor = '';
    });
  });
}

function filterMapFeatures(){
  // checkdates
  var sitesFiltered=[]

  $.each(Object.keys(resultsData),function(i,thisSite){
    if(new Date(resultsData[thisSite].minDate).getYear()+1900>=minYear){
      sitesFiltered.push(thisSite)
    }
  })


  filter=['all',['in','MonitoringLocationIdentifier'].concat(sitesFiltered)]

  var filteredSites=filterGeojson(sitesFiltered)

  map.fitBounds(turf.bbox(filteredSites),{
    padding:20
  })

  map.setFilter('sites', filter)
}

function filterGeojson(sitesFiltered){
  var filteredSites=siteLocations;
  var newFeatures=[]
  filteredSites.features.forEach(function(thisSite){
    if(sitesFiltered.indexOf(thisSite.properties.MonitoringLocationIdentifier) > -1){
      newFeatures.push(thisSite)
    }
  })
  filteredSites.features=newFeatures
  return(filteredSites)
}
