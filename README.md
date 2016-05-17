* branch ```pythonreact``` <= python-react pip package
* branch ```reactrender``` <= react-render pip package
* branch ```master ``` <= django-react library


***


### Python-react

>Apps like django-pipeline and django-compressor have done a great job with static assets. I’ve been a great fan of django-pipeline actually but I hate how they take away all the transparency in order to make things a bit magical. They are limited in what they can do by the staticfiles system. They are opaque and make it harder to debug problems. They also need companion apps for to integrate any new javascript tool like gulp or browserify. Even after having all these wrappers, the experience can be quite rough at times. Documentation and resources available for javascript tools are not directly applicable sometimes when using these wrappers. You’ve an additional layer of software and configuration to worry about or wonder how your python configuration translates to the javascript. Things can be much better. - Owais Lone

### Rendering

Server-side rendering is a very simple concept -- you create a node.js server that looks for Reactjs components, renders them (usually using ```React.renderToString```) and returns the output in HTML format. All that is required is a node server (```render.js```) and a ```package.json``` file with its dependencies. Babel is used as well in order to transform JSX into JS and ES6 into ES5.

Projects like ```react-render``` ([repo](https://github.com/mic159/react-render/)), and ```python-react``` ([repo](https://github.com/markfinger/python-react)), allow the user to input the prerendered JSX through native python, which is then caught by the node server, which uses json to render the JSX, along with the python package ```requests``` to return it as a string. This allows the code to look like more native python:

```Python
from react_render.django.render import render_component

props = {
    'foo': 'bar',
    'woz': [1,2,3],
}

rendered = render_component('path/to/component.js', props=props)

print(rendered)
```

### Simplify

This is great, but how do you keep track of all the JSX files? If you decide to use React as your front end, something like [webpack](https://webpack.github.io/) is the way to go. Using webpack, you can setup an entry point for your files, and it will bundle them all together, allowing the node server to render the bundle instead of each file indivdually. My current webpack config looks like this:

```Javascript
[]...
module.exports = [
  // Client side
{
  context: __dirname,
  entry: {
    'main': ['./assets/js/index.js']
  },
  output: {
      path: path.resolve('./assets/bundles/'),
      filename: "[name].js",
      library: 'main'
  },
  module: moduleOpts,
 },
  // Server side
 {
    context: __dirname,
    entry: {
      'main': ['./assets/js/components/app.jsx']
    },
    output: {
      path: path.resolve('./assets/bundles/'),
      filename: '[name].server.js',
      libraryTarget: 'commonjs2'
    },
    module: moduleOpts
}]
```

Notice the comments? Using webpack allows the developer to use one bundle for frontend, and also create a backend bundle for server-side rendering. For Django, you would use [django-webpack-loader](https://github.com/owais/django-webpack-loader). This completely replaces staticfiles, and treats Django as only an API. From the article, it is best practice to have a dev webpack config, local, and prod.

### Issues
One of the more troubling issues when integrating React are forms. As you know, Django requires a ```csrf``` token in each form which [most examples](https://github.com/mic159/react-render/blob/master/example/example_app/static/jsx/components/CommentForm.jsx) don't contain. A simple way to do this is to wrap it up as a reusable React component:

```Javascript
var React = require('react');
var DjangoCSRFToken = React.createClass({
  render: function() {
    var csrfToken = Django.csrf_token();
    return React.DOM.input(
      {type:"hidden", name:"csrfmiddlewaretoken", value:csrfToken}
      );
  }
});
module.exports = DjangoCSRFToken: DjangoCSRFToken;
```
You can use the jQuery package cookie to retrieve the token:

```Javascript
var csrftoken = $.cookie('csrftoken');
```
Or, use native Django (which still needs jQuery):

```Javascript
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
                  );
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
```
Save that into a new JS module, and then include it like so:

```Javascript
return (
       <form method='post' action={this.props.acceptUrl}>
         <DjangoCSRFToken />
         <input type="text" name="edit_id" value={edit.id} />
         <input type="submit" name="accept" value="Accept" />
       </form
       );
```

### Install

```
virtualenv venv
pip install -r requirements
npm install
npm run build

./manage runserver 8002
npm run react-service
```

### Pythonflow
- Python HTTP API sends bundle to node server
- Node server recieves component
- Returns rendered bundle
- Import and use in templates

## V2

When researching ways to make JSX deployment easier for designers, I found [react-router](https://github.com/reactjs/react-router), which, in combination with webpack and a node server (probably express.js), was the missing piece in order to really integrate Reactjs as a frontend by replacing urls.py as well. In order for this to work, the Django app must use DRF (or some form of an API), and react-router + webpack + a render service = the full front end suite. Here's a quick example pulled from example code from their repo which shows how powerful the library is at replacing Django's routing service:

```Javascript
render((
  <Router history={browserHistory}>
    <Route path="/" component={App}>
      <Route path="about" component={About}/>
      <Route path="users" component={Users}>
        <Route path="/user/:userId" component={User}/>
      </Route>
      <Route path="*" component={NoMatch}/>
    </Route>
  </Router>
), document.body)
```

### Javascriptflow
With this, the workflow goes along these lines:

- Designer writes .jsx file
- Adds the file to js/components, and builds the webpack
- appropriate edits are made to router file, which pulls from the Django API

The .jsx file acts like this:

- Originally written as a component (keeping it DRY)
- Bundled with webpack
- Is rendered by node.js server
- Content is returned to client
- *content can be cached, allowing quicker page load speeds

Obviously, this is a much larger project, but with is more flexible from a designing perspective, ***WHY***

With this workflow, the normal webpack template tags would be used to replace the HTML:

```HTML
{% load render_bundle from webpack_loader %}
<html>
  <head>
    {% render_bundle 'main' 'css' %}
  </head>
  <body>
    ....
    {% render_bundle 'main' 'js' %}
  </body>
</head>
```

In order to pass props through the components (since you would no longer declare them in views.py, you'd implement this:

```Javascript
var Dashboard = require('./Dashboard');
var Comments = require('./Comments');
var RouteHandler = require('react-router/modules/mixins/RouteHandler');

var Index = React.createClass({
      mixins: [RouteHandler],
      render: function () {
        var handler = this.getRouteHandler({ myProp: 'value'});
        return (
            <div>
                <header>Some header</header>
                {handler}
           </div>
        );
  }
});
var routes = (
  <Route path="/" handler={Index}>
    <Route path="comments" handler={Comments}/>
    <DefaultRoute handler={Dashboard}/>
  </Route>
);
ReactRouter.run(routes, function (Handler) {
  React.render(<Handler/>, document.body);
});
```

### Conclusion

After much research and toying with different tools, using a node.js service like [react-render](https://github.com/mic159/react-render) along with webpack is the best solution for replacing Django's frontend. Using Django solely as an API once React has been implemented is also best practice (remember, JSX files render both JS and HTML). Webpack rocks, and React is the future of front end. Thanks for reading :)
