(function() {
"use strict";

App.confirm_before_submit = function(selector, message) {
  $(selector).submit(function(evt) {
    if(! confirm(message)) {
      evt.preventDefault();
    }
  });
};

App.confirm_before_click = function(selector, message) {
  $(selector).click(function(evt) {
    if(! confirm(message)) {
      evt.preventDefault();
    }
  });
};

})();
