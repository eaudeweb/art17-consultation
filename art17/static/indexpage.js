(function() {
"use strict";


_($('.records-commentstatus [name=status]')).forEach(function(el) {
  var hidden_input = $(el);
  var data = _(App.STATUS_OPTIONS).map(function(item) {
    return {id: item[0], text: item[1]};
  });
  hidden_input.select2({
    data: data,
    formatSelection: function(ob) { return ob.text.split(' ')[0]; },
    minimumResultsForSearch: -1,  // disable search field
    width: '5em',
    dropdownAutoWidth: true
  });
});


$('.records-commentstatus').change(function(evt) {
  var form = $(this);
  var select = form.find('.select2-container');
  select.hide();
  form.append('...').submit();
});


$('.records-commentdelete').submit(function(evt) {
  if(! confirm("Ștergi comentariul?")) {
    evt.preventDefault();
  }
});


$('.helpbox-button').click(function(evt) {
  evt.preventDefault();
  $('#helpbox').modal();
});


})();
