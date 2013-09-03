(function(App, Backbone, $) {
"use strict";


App.AjaxSelect = Backbone.View.extend({
    initialize: function() {
        this.update();
    },

    get_options: function() {
        var rv = new $.Deferred();

        var url = this.options.get_data_url();
        if(url) {
            $.get(url, function(resp) {
                rv.resolve(resp.options);
            });
        }
        else {
            rv.resolve([]);
        }

        return rv;
    },

    render_options: function(options) {
        this.$el.select2('destroy');
        this.$el.select2({
            data: [{id: '', text: "toate"}].concat(options),
            width: this.options.width
        });
    },

    update: function() {
        this.$el.select2('val', '');
        this.get_options().done(_.bind(this.render_options, this));
    }
});


})(window.App, window.Backbone, window.jQuery);
