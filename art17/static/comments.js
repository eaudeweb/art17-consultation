(function() {

"use strict";

var table = $('table.records');


table.on('click', '.records-commentbtn', function(evt) {
  var tr = $(evt.target).parents('table.records tr');
  var comment_tr = (table.find('.comment-template')
                    .clone().removeClass('comment-template'));
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
    data[input.attr('name')] = input.val();
  });

  var save_button = comment_tr.find('.comment-save');
  save_button.attr('disabled', 'disabled');
  save_button.empty().append("salvez ",
                             $('<i>', {class: 'icon-spinner icon-spin'}));

  console.log(data);
});

})();
