App = Ember.Application.create();

App.Router.map(function() {
  // put your routes here
  this.resource("pages", {path: '/:site_name'}, function(){
    this.resource("page", {path: '/:page_no'});
  });
});


App.ApplicationRoute = Ember.Route.extend({
  model: function() {
    var site_names = [];
    ['sw', 'cs', 'news'].forEach(function(site_name) {
      var pages = App.PagesController.create({
        site_name: site_name
      });
      site_names.pushObject(pages);
    });
    return site_names;
  }
});

App.PagesRoute = Ember.Route.extend({
  model: function(params) {
    var content = [];
    $.getJSON("http://localhost:8080/api/%@1/5".fmt(params.site_name), function(results) {
      results.pages.forEach(function(news) {
        var n = App.NewsPage.create({
          title: news.title,
          content: news.content,
          create_at: news.create_at
        });
        content.pushObject(n);
      });
    });
    return content;
  }
});

App.PagesController = Ember.ArrayController.extend({
});

App.Pages = Ember.Object.extend({
  site_name: ''
});

App.NewsPage = Ember.Object.extend({
  title: null,
  content: null,
  create_at: null,
  intro: function(){

  }
});

Ember.Handlebars.registerBoundHelper('highlight', function(value, options) {
  var escaped = Handlebars.Utils.escapeExpression(value);
  return new Handlebars.SafeString('<span class="highlight">' + escaped + '</span>');
});


/* make bootstrap navlist response to link active from Emberjs.*/

App.NavListView = Ember.View.extend({
  tagName: 'li',
  classNameBindings: 'active'.w(),

  didInsertElement: function () {
      this._super();
      this.notifyPropertyChange('active');
      var _this = this;
      this.get('parentView').on('click', function () {
          _this.notifyPropertyChange('active');
      });
  },

  active: function () {
      return this.get('childViews.firstObject.active');
  }.property()
});
