function uiInits(){

  $("#minDateSelect").datepicker({
      'dateFormat': "mm/dd/yyyy",
      'minDate':new Date(minDate),
      'maxDate':new Date(maxDate),
      'defaultDate':new Date(minDate),
      'setDefaultDate':true,
   })
   .on('change',function(){
     minDate=$(this).val()
     dateChangeEvent()
   })
   $("#maxDateSelect").datepicker({
       'dateFormat': "mm/dd/yyyy",
       'minDate':new Date(minDate),
       'maxDate':new Date(maxDate),
       'defaultDate':new Date(maxDate),
       'setDefaultDate':true,
    })
    .on('change',function(){
      maxDate=$(this).val()
      dateChangeEvent()
    })

}
