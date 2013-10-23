(function() {
"use strict";

$('.records').on('click', '.records-repliesbtn', function(evt) {
  evt.preventDefault();
  var link = $(this);
  var url = link.attr('href');
  var title = "Replici";
  var params = 'height=600,width=600,screenX=300,screenY=100';
  var popup = window.open(url, title, params);
  popup.focus();
});


$('body').on('click', '.readbox-mark', function(evt) {
  evt.preventDefault();
  var button = $(this);
  var reply = button.parents('.reply');
  var reply_id = reply.data('id');
  var post = $.post(App.set_read_status_url,
                    {reply_id: reply_id, read: 'on'});
  post.done(function() {
    reply.addClass('reply-read');
  });
});


$('body').on('click', '.readbox-unmark', function(evt) {
  evt.preventDefault();
  var button = $(this);
  var reply = button.parents('.reply');
  var reply_id = reply.data('id');
  var post = $.post(App.set_read_status_url,
                    {reply_id: reply_id});
  post.done(function() {
    reply.removeClass('reply-read');
  });
});

})();
