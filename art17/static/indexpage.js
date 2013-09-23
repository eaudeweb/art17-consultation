(function() {
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


App.species_filter = function(species_groups, species_list) {
  var speciesfilter = $('.speciesfilter');

  var group_select = speciesfilter.find('[name=group]').select2({
    data: species_groups,
    minimumResultsForSearch: -1,  // disable search field
    width: '10em'
  });


  var species_select = speciesfilter.find('[name=species]');

  function update_species_select(group_id) {
    var group_id = group_select.select2('val');
    var species_in_group = _(species_list).filter(
        function(sp){return sp.group_id == group_id});

    species_select.select2('destroy').select2({
      data: species_in_group,
      multiple: false,
      width: '22em'
    });

    App.region_select.update();
  }

  App.region_select = new App.AjaxSelect({
    el: speciesfilter.find('[name=region]'),
    get_data_url: function() {
       var species_code = species_select.val();
       return species_code ? 'regiuni/' + species_code : null;
    },
    width: '10em'
  });


  update_species_select();

  speciesfilter.on('change', '[name=group]', function() {
    species_select.select2('val', '');
    update_species_select();
  });

  speciesfilter.on('change', '[name=species]', function() {
    App.region_select.update();
  });
};


App.habitat_filter = function(habitat_list) {
  var habitatfilter = $('.habitatfilter');

  var habitat_select = habitatfilter.find('[name=habitat]').select2({
    data: habitat_list,
    width: '30em'
  });

  App.region_select = new App.AjaxSelect({
    el: habitatfilter.find('[name=region]'),
    get_data_url: function() {
       var habitat_code = habitat_select.val();
       return habitat_code ? 'regiuni/' + habitat_code : null;
    },
    width: '15em'
  });

  habitat_select.change(function() {
    App.region_select.update();
  });
};


$('body').on('click', '.showmap', function(evt) {
  evt.preventDefault();
  var link = $(this);
  var url = link.attr('href');
  var title = "Hartă";
  var params = 'height=650,width=850,screenX=100,screenY=100';
  var popup = window.open(url, title, params);
  popup.focus();
});


_($('.records-conclusionstatus [name=status]')).forEach(function(el) {
  var hidden_input = $(el);
  var select = $('<select name="status">');
  _(App.STATUS_OPTIONS).forEach(function(item) {
    var value = item[0];
    var label = item[1];
    var option = $('<option>', {value: value});
    option.text(label);
    if(hidden_input.val() == value) {
      option.attr('selected', true);
    }
    select.append(option);
  });
  hidden_input.replaceWith(select);
});


$('.records-conclusionstatus').change(function(evt) {
  var form = $(this);
  var select = $(evt.target);
  select.hide();
  form.append('...').submit();
});


$('.records-conclusiondelete').submit(function(evt) {
  if(! confirm("Ștergi concluzia?")) {
    evt.preventDefault();
  }
});

})();