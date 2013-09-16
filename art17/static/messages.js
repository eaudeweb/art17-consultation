(function() {
"use strict";

$('.records').on('click', '.records-messagesbtn', function(evt) {
  evt.preventDefault();
  var link = $(evt.target);
  var url = link.attr('href');
  var title = "Mesaje";
  var params = 'height=600,width=600,screenX=300,screenY=100';
  var popup = window.open(url, title, params);
  popup.focus();
});

})();
