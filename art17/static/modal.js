(function() {

"use strict";

var recorddetail = $('#recorddetail-modal');

$('.records-detailbtn').click(function(evt) {
  evt.preventDefault();
  var url = $(this).attr('href');

  recorddetail.modal('hide');
  set_html("<h1>Se încarcă...</h1>");
  $.get(url).done(set_html);
  recorddetail.modal();
});

function set_html(html) {
  var title = recorddetail.find('.recorddetail-title');
  var body = recorddetail.find('.recorddetail-body');
  body.html(html);
  var h1 = body.find('h1').remove();
  title.empty().append(h1.html());
}

})();
