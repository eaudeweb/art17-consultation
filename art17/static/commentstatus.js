(function() {
"use strict";

var menu_items = [
  {value: 'new', label: "nou"},
  {value: 'approved', label: "aprobat"},
  {value: 'rejected', label: "refuzat"}
];


_($('.records-commentstatus [name=status]')).forEach(function(el) {
  var hidden_input = $(el);
  var select = $('<select name="status">');
  _(menu_items).forEach(function(item) {
    var option = $('<option>', {value: item.value});
    option.text(item.label);
    if(hidden_input.val() == item.value) {
      option.attr('selected', true);
    }
    select.append(option);
  });
  hidden_input.replaceWith(select);
});


$('.records-commentstatus').change(function(evt) {
  var form = $(this);
  var select = $(evt.target);
  select.hide();
  form.append('...').submit();
});

})();
