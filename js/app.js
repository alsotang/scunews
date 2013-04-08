App = Ember.Application.create();

App.sites = ['sw', 'cs', 'news', 'seei'];

App.apiURL = window.location.href + 'api';
App.pageCount = '5';

App.PagesController = Ember.ArrayController.extend({
  content: [],
  loadingWhich: '',
  loadPages: function(view) {
    this.set('loadingWhich', view);
    this.set('content', []);
    App.pageController.switchPage({});

    var _this = this;
    $.getJSON("%@/%@/%@".fmt(App.apiURL, view, App.pageCount), function(results) {
      if(_this.get('loadingWhich') !== view) {
        return;
      } else {
        _this.set('loadingWhich', '');
      }
      $.each(results.pages, function(i, page) {
        _this.pushObject(page);
      });

      App.pageController.switchPage(_this.get('content')[0]);
    });
  }
});

App.pagesController = App.PagesController.create();

App.PageController = Ember.ObjectController.extend({
  switchPage: function(page) {
    this.set('content', page);
  }
});

App.pageController = App.PageController.create();

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



