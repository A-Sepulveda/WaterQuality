function uiInits(){


  minYear=1900+minDate.getYear()
  maxYear=1900+maxDate.getYear()

  var yearSpread=[...Array(maxYear-minYear+1)].map((_, i) => i + minYear)

  yearSpread.forEach(function(year) {
    // console.log(year);
    if(year==minYear){
      $('#yearsDropdown').append("<option value="+year+" selected>"+year+"</option>")
    }else{
      $('#yearsDropdown').append("<option value="+year+">"+year+"</option>")
    }

  });
  $('#yearsDropdown').formSelect()

  $('#yearsDropdown').change(function(){
    minYear=$(this).val()
    console.log(minYear);
    filterMapFeatures();
  })






}
