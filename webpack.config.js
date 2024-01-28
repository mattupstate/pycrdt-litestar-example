const path = require("path");
const webpack = require("webpack");
const BundleTracker = require("webpack-bundle-tracker");
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

module.exports = {
    context: __dirname,
    entry: {
        "main": "./example_app/static/src/js/index.js",
    },
    output: {
        path: path.resolve(__dirname, "example_app/static/bundles/"),
        filename: "[name]-[contenthash].js",
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.ttf$/,
                type: 'asset/resource'
            }
        ]
    },
    plugins: [
        new BundleTracker({ path: __dirname, filename: "webpack-stats.json" }),
        new WebpackManifestPlugin({
            publicPath: "static/bundles"
        }),
    ],
};