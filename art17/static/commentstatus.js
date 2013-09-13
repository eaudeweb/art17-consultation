(function() {
"use strict";

$('.records-commentstatus').change(function(evt) {
  var form = $(this);
  var select = $(evt.target);
  select.hide();
  form.append('...').submit();
});

})();
