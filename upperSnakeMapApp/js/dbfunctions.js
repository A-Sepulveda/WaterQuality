function wqquery(){
  $('#loader').show()
  axios.get('https://gappadus.services/postgres/', {
    params: {
      type:'waterquality',
      queryString: 'select * from waterquality;'
    }
  }).then(function (result) {
    $('#loader').hide()
    console.log(result.data);
  }).catch(function (error) {
    $('#loader').hide()
    console.log("error:", error);
  });
}

function getMeanValues(){
  $('#loader').show()
  axios.get('https://gappadus.services/postgres/', {
    params: {
      type:'waterquality',
      queryString: 'SELECT siteid, AVG (camean) AS camean FROM waterquality WHERE tempmean IS NOT NULL and camean IS NOT NULL AND EXTRACT(MONTH FROM date) in (6,7,8,9) GROUP BY siteid;'
    }
  }).then(function (result) {
    $('#loader').hide()
    console.log(result.data);
  }).catch(function (error) {
    $('#loader').hide()
    console.log("error:", error);
  });
}
