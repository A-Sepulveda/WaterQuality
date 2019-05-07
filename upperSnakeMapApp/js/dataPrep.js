var resultsData={}

function dataPrep(){
  console.log(resultsSample)
  $.each(resultsSample,function(i,obs){
    var thisLocationId=obs.MonitoringLocationIdentifier
    thisDate=obs.ActivityStartDate
    if(resultsData[thisLocationId]){
      if(resultsData[thisLocationId][thisDate]){
        resultsData[thisLocationId][thisDate].push(obs)
      }else{
        resultsData[thisLocationId][thisDate]=[obs]
      }
    }else{
      resultsData[thisLocationId]={
        thisDate:[obs]
      }

    }
  })
}
