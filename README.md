## rendered-react-django

React is a MVC framework javascript library for building user interfaces. Although tempting, the use of react wrecks an apps SEO. The package react-python allows the rendering of react components to occur on the server side. Here's the github [repository](https://github.com/mic159/react-render) for django-react.

This project is an example of using react components using this package. It uses Material-UI to follow Google's material guidelines. It's pretty.


https://github.com/owais/django-webpack-loader

### JSX

JSX is a javascript extension that looks like XML but can render both HTML and React components. It is reccommended due to its more concise and familiar syntax for definging tree structures with attributes -- this is the equivilant to the props argument using react-python.

```javascript
var Nav, Profile;
// Input (JSX):
var app = <Nav color="blue"><Profile>click</Profile></Nav>;
// Output (JS):
var app = React.createElement(
  Nav,
  {color:"blue"},
  React.createElement(Profile, null, "click")
);
```

Example of a form written in JSX

```javascript
var Form = MyFormComponent;

var App = (
  <Form>
    <Form.Row>
      <Form.Label />
      <Form.Input />
    </Form.Row>
  </Form>
);
```

### Dependencies

The purpose of python-react is to replace the django template system with react components. The package has multiple node dependencies, and requires a render server in order to render the components on the server-side. So, implementing this package would affect:

- The way Django templates are used. A ```{% rendered raw %}``` tag would replace any HTML (React can render JSX into native HTML if we don't want to include any react components but want to stay consistent with the template style).

- An extra proccess to render the components. Best to use Supervisor to run the render server in the background consistently. We can also wrap the call to the server to first check if the data is cached locally and populate the rendered markup with that data to ease the load.

### Passing in data

python-react takes a dictionary of data that can be passed through the renderer for use on the client side, i.e.:


```Javascript
render_component(
    path='',

    props={
        'foo': 'bar'
    },
```

Another package that renders React components on the server is [react-render](https://github.com/mic159/react-render). It inherits much of its code from python-react, but is specific to Django projects.

### django-webpack-loader

The other direction to go in is using a module bundler like webpack. The package [django-webpack-loader](https://github.com/owais/django-webpack-loader/) consumes bundles (i.e. React components) and generates static bundles that can then be used in Django templates. [This writeup](http://owaislone.org/blog/webpack-plus-reactjs-and-django/) does a great job at explaining the relationship between webpack, react and django.

React.js also has a [tutorial](http://reactjs.net/guides/webpack.html) regarding the use of webpack to render bundles on the server side. This may be the preferred approach, as it allows:

- frontend engineers and designers to run webpack mode in watch mode
- use grunt, gulp, or any dev server without limitations
- makes it easy to use npm or bower as a package manager

The limitations to this approach over something like python-react include:

- decouples frontend django and backend, making it harder to store static files in app directories (although changing to this workflow is more awesome)
- That's about all, folks

[Modern frontends with Django](http://owaislone.org/blog/modern-frontends-with-django/) along with [Webpack plus hot react components](http://owaislone.org/blog/webpack-plus-reactjs-and-django/) are great starting points. The packages used for this approach include

- [webpack-bundle-tracker](https://github.com/owais/webpack-bundle-tracker)
- [https://github.com/owais/django-webpack-loader/](https://github.com/owais/django-webpack-loader/)

### How to Install

_currently does not run correctly, migrating from python-react to django-webpack-loader_

```
pip install requirements
cd react
npm install
node server.js
cd ..
manage.py runserver
```

```HTML
{% load render_bundle from webpack_loader %}
<html>
  <head>
    <meta charset="UTF-8">
    <title>Django, Webpack and ReactJS</title>
    {% render_bundle 'main' 'css' %}
  </head>
  <body>
     <!-- Using django-webpack-loader -->
     {% render_bundle 'main' 'js' %}

     <!-- react-render options below -->
     {{ my_component }}
     <!-- .render_props outputs JSON serialized props.
     This allows you to reuse the encoded form of your props on the client-side.
     -->
      <script>
        var myProps = {{ my_component.render_props }};
      </script>
  </body>
</html>
```
