function confirm_before_submit(selector, message) {
  $(selector).submit(function(evt) {
    if(! confirm(message)) {
      evt.preventDefault();
    }
  });
}

function confirm_before_click(selector, message) {
  $(selector).click(function(evt) {
    if(! confirm(message)) {
      evt.preventDefault();
    }
  });
}
