var React = require('react');
var csrftoken = $.cookie('csrftoken');

var DjangoCSRFToken = React.createClass({

  render: function() {

    var csrfToken = Django.csrf_token();

    return React.DOM.input(
      {type:"hidden", name:"csrfmiddlewaretoken", value:csrfToken}
      );
  }
});

module.exports = DjangoCSRFToken: DjangoCSRFToken;
