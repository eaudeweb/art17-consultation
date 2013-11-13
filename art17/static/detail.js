(function() {

"use strict";

var recorddetail = $('#recorddetail-modal');

$('.records-detailbtn').click(function(evt) {
  evt.preventDefault();
  var url = $(this).data('url');

  recorddetail.modal('hide');
  set_html("<h1>Se încarcă...</h1>");
  $.get(url).done(set_html);
  recorddetail.modal();
});

function set_html(html) {
  var title = recorddetail.find('.modal-title');
  var body = recorddetail.find('.modal-body');
  body.html(html);
  var h1 = body.find('h1').remove();
  title.empty().append(h1.html());
}

$('body').on('click', '.showmap', function(evt) {
  evt.preventDefault();
  var link = $(this);
  var url = link.attr('href');
  var title = "Hartă";
  var params = 'height=650,width=850,screenX=100,screenY=100';
  var popup = window.open(url, title, params);
  popup.focus();
});

})();
