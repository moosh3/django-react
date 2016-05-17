var path = require("path");
var webpack = require("webpack")

var moduleOpts = {
    // don't parse jQuery for times sake
    noParse: [
      /jquery/
    ],
    // use babel loader when using jsx files
    loaders: [
      {test: /\.jsx$/, exclude: /node_modules/, loader: 'babel'}
    ]
};

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
