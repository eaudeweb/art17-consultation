(function() {
"use strict";

$('.records').on('click', '.records-repliesbtn', function(evt) {
  evt.preventDefault();
  var link = $(this);
  var url = link.attr('href');
  var title = "Replici";
  var params = 'height=600,width=600,screenX=300,screenY=100,scrollbars=1';
  var popup = window.open(url, title, params);
  popup.focus();
});

})();
