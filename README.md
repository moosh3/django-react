

>Apps like django-pipeline and django-compressor have done a great job with static assets. I’ve been a great fan of django-pipeline actually but I hate how they take away all the transparency in order to make things a bit magical. They are limited in what they can do by the staticfiles system. They are opaque and make it harder to debug problems. They also need companion apps for to integrate any new javascript tool like gulp or browserify. Even after having all these wrappers, the experience can be quite rough at times. Documentation and resources available for javascript tools are not directly applicable sometimes when using these wrappers. You’ve an additional layer of software and configuration to worry about or wonder how your python configuration translates to the javascript. Things can be much better. - Owais Lone
### Rendering

Server-side rendering is a very simple concept -- you create a node.js server that looks for Reactjs components, renders them (usually using ```React.renderToString```) and returns the output in HTML format. This is very simple and can be implemented without the use of other packages. All that is required is a node server (```render.js```) and a ```package.json``` file with its dependencies. Babel is used as well in order to transform JSX into JS and ES6 into ES5 (letting us use 'tomorrows features, today').

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

### Conclusion
- Python HTTP API sends bundle to node server
- Node server recieves component
- Returns rendered bundle
- Import and use in templates

After much research and toying with different tools, using a node.js service like [react-render](https://github.com/mic159/react-render) along with webpack is the best solution for replacing Django's frontend. Using Django solely as an API once React has been implemented is also best practice (remember, JSX files render both JS and HTML). Webpack rocks, and React is the future of front end. Thanks for reading :)
