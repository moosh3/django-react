var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

const config = {
  context: __dirname,
  entry: './assets/js/index',
  output: {
      path: path.resolve('./assets/webpack_bundles/'),
      filename: "[name]-[hash].js"
  },

  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ]
}

module.exports = config;
