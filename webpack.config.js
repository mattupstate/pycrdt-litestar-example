const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const { WebpackManifestPlugin } = require("webpack-manifest-plugin");

module.exports = {
  context: __dirname,
  entry: {
    main: "./static/js/index.js",
  },
  output: {
    path: path.resolve(__dirname, "./dist/js"),
    filename: "[name]-[contenthash].js",
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"],
      },
      {
        test: /\.ttf$/,
        type: "asset/resource",
      },
    ],
  },
  plugins: [
    new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
    new WebpackManifestPlugin({
      publicPath: "static/js",
    }),
  ],
};
