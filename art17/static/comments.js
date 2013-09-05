(function() {

"use strict";

var recordcomment = $('#recordcomment-modal');


function show_comment_form(html, url) {
  set_html(html);
  var form = recordcomment.find('form');
  form.submit(function(evt) {
    evt.preventDefault();
    var form = $(evt.target);
    var pairs = form.serializeArray();
    var data = _.object(_(pairs).pluck('name'),
                        _(pairs).pluck('value'));

    $.post(url, data).done(function(html) {
      show_comment_form(html, url);
    });

  });
}


$('.records-commentbtn').click(function(evt) {
  evt.preventDefault();
  var url = $(this).data('url');

  recordcomment.modal('hide');
  set_html("<h1>Se încarcă...</h1>");
  $.get(url).done(function(html) {
    show_comment_form(html, url);
  });
  recordcomment.modal();
});


function set_html(html) {
  var title = recordcomment.find('.recordcomment-title');
  var body = recordcomment.find('.recordcomment-body');
  body.html(html);
  var h1 = body.find('h1').remove();
  title.empty().append(h1.html());
  var footer = recordcomment.find('.recordcomment-footer');
  footer.find('.recordcomment-save').remove();
  footer.append(body.find('.recordcomment-save').clone().click(function() {
    body.find('form').submit();
  }));
}

})();
