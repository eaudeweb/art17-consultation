(function() {

"use strict";

var table = $('table.records');


function icon(cls) {
  return $('<i>', {class: cls});
}


table.on('click', '.records-commentbtn', function(evt) {
  var button = $(evt.target);
  var tr = button.parents('table.records tr');
  var comment_tr = table.find('.comment-template').clone();
  var saveurl = button.data('saveurl');
  comment_tr.removeClass('comment-template');
  comment_tr.data('saveurl', saveurl);
  comment_tr.find('input').attr('size', 1);  // so they have a small min width
  comment_tr.insertAfter(tr);
});


table.on('click', '.comment-cancel', function(evt) {
  $(evt.target).parents('table.records tr').remove();
});


table.on('click', '.comment-save', function(evt) {
  var comment_tr = $(evt.target).parents('.comment');
  var data = {};
  _(comment_tr.find(':input')).forEach(function(el) {
    var input = $(el);
    var name = input.attr('name');
    if(name) {
      data[name] = input.val();
    }
  });

  var save_button = comment_tr.find('.comment-save');
  save_button.attr('disabled', 'disabled');
  save_button.empty().append("salvez ", icon('icon-spinner icon-spin'));

  var request = $.ajax({
    type: 'POST',
    url: comment_tr.data('saveurl'),
    data: JSON.stringify(data),
    contentType: 'application/json'
  });

  request.done(function() {
    save_button.empty().append("ok ", icon('icon-check'));
    setTimeout(function() {
      comment_tr.fadeOut(500, function() {
        comment_tr.remove();
      });
    }, 500);
  });
});


var recordcomment = $('#recordcomment-modal');

$('.records-commentbtn').click(function(evt) {
  evt.preventDefault();
  var url = $(this).data('url');

  recordcomment.modal('hide');
  set_html("<h1>Se încarcă...</h1>");
  $.get(url).done(function(resp) {
    set_html(resp['html']);
  });
  recordcomment.modal();
});

function set_html(html) {
  var title = recordcomment.find('.recordcomment-title');
  var body = recordcomment.find('.recordcomment-body');
  body.html(html);
  var h1 = body.find('h1').remove();
  title.empty().append(h1.html());
}

})();
