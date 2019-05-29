var riskLookup={}
var selectedAnalyte='ca'

function filterChange(){
  console.log(minYear)
  console.log(selectedAnalyte)
  getMeanValues();
}

function getSiteRisk(){
  riskLookup={}
  queryResult.forEach(function(thisSite){
    var siteId=thisSite.siteid;
    var thisRisk=caRisk(Number(thisSite.camean))
    riskLookup[siteId]=thisRisk
  })
  filterRiskMapFeatures()
}

function caRisk(d) {
    return d > 28 ? 'veryHigh' :
           d >= 20  ? 'high' :
           d >= 12  ? 'moderate' :
           d >= 0  ? 'low' :
                      'na';
}

$(document).ready(function() {
  // dataPrep();
  getDateRange();
});
