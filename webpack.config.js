var path = require("path");
var webpack = require("webpack")
var BundleTracker = require('webpack-bundle-tracker');

var moduleOpts = {
    noParse: [
      /jquery/
    ],

    loaders: [
      {test: /\.jsx$/, exclude: /node_modules/, loader: 'babel'}
    ]
};

plugins: [
  new BundleTracker({filename: 'webpack-stats.json'})
],

module.exports = [
  // Client side
{
  context: __dirname,
  entry: {
    'main': ['./assets/js/index']
  },
  output: {
      path: path.resolve('./assets/bundles/'),
      filename: "[name]-[hash].js",
      library: 'main'
  },
  module: moduleOpts,
  devtool: 'eval'
 },
  // Server side
 {
    context: __dirname,
    entry: {
      'main': ['./assets/js/components/CommentBox.jsx']
    },
    output: {
      path: path.resolve('./assets/bundles/'),
      filename: '[name]-[hash].server.js',
      libraryTarget: 'commonjs2'
    },
    module: moduleOpts
}],
