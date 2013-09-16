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


$('body').on('click', '.readbox-mark', function(evt) {
  evt.preventDefault();
  var button = $(evt.target);
  var message = button.parents('.message');
  var message_id = message.data('id');
  var post = $.post(App.set_read_status_url,
                    {message_id: message_id, read: 'on'});
  post.done(function() {
    message.addClass('message-read');
  });
});


$('body').on('click', '.readbox-unmark', function(evt) {
  evt.preventDefault();
  var button = $(evt.target);
  var message = button.parents('.message');
  var message_id = message.data('id');
  var post = $.post(App.set_read_status_url,
                    {message_id: message_id});
  post.done(function() {
    message.removeClass('message-read');
  });
});

})();
