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

})();
