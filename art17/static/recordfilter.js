(function(App, Backbone, $) {
"use strict";


App.RegionSelect = Backbone.View.extend({
    initialize: function() {
        this.update();
    },

    get_options: function() {
        var rv = new $.Deferred();

        var url = this.options.get_data_url();
        if(url) {
            $.get(url, function(resp) {
                rv.resolve(resp.regions);
            });
        }
        else {
            rv.resolve([]);
        }

        return rv;
    },

    render_regions: function(regions) {
        this.$el.select2('destroy');
        this.$el.select2({
            data: [{id: '', text: "toate"}].concat(regions),
            width: this.options.width
        });
    },

    update: function() {
        this.$el.select2('val', '');
        this.get_options().done(_.bind(this.render_regions, this));
    }
});


})(window.App, window.Backbone, window.jQuery);
