/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

"use strict";

const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const RemoveEmptyScriptsPlugin = require("webpack-remove-empty-scripts");
const TerserPlugin = require("terser-webpack-plugin");
const path = require("path");

module.exports = {
    entry: {
        "protocol-base": "./src/js/protocol/base.js",
        "protocol-global": "./src/js/protocol/global.js",
        "protocol-mozilla-theme": "./src/css/protocol/mozilla.scss",
        "protocol-firefox-theme": "./src/css/protocol/firefox.scss",
        "protocol-navigation-css":
            "./src/css/protocol/components/navigation.scss",
        "protocol-navigation-js": "./src/js/protocol/components/navigation.js",
        "protocol-footer-css": "./src/css/protocol/components/footer.scss",
        "protocol-footer-js": "./src/js/protocol/components/footer.js",
        "protocol-split": "./src/css/protocol/components/split.scss",
        "protocol-card": "./src/css/protocol/components/card.scss",
    },
    output: {
        filename: "js/[name].js",
        path: path.resolve(__dirname, "birdbox/birdbox/static/"),
        publicPath: "/static/",
    },
    optimization: {
        minimizer: [
            new TerserPlugin({
                terserOptions: { ie8: true },
            }),
            new CssMinimizerPlugin({}),
        ],
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                include: path.resolve(__dirname, "src"),
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: [
                            [
                                "@babel/preset-env",
                                {
                                    targets: {
                                        ie: "10",
                                    },
                                },
                            ],
                        ],
                    },
                },
            },
            {
                test: /\.scss$/,
                include: path.resolve(__dirname, "src"),
                exclude: /node_modules/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: "css-loader",
                        options: {
                            url: false,
                        },
                    },
                    "sass-loader",
                ],
            },
        ],
    },
    watchOptions: {
        aggregateTimeout: 600,
        ignored: "/node_modules/",
    },
    performance: {
        hints: "warning",
    },
    devServer: {
        port: 8000,
        open: false,
        hot: false,
        static: false,
        devMiddleware: {
            index: false, // specify to enable root proxy'ing
        },
        proxy: {
            context: () => true,
            target: "http://0.0.0.0:8080",
        },
        watchFiles: ["src/**/*.js", "src/**/*.scss", "birdbox/**/*.html"],
        client: {
            logging: "error",
            overlay: false,
        },
        setupExitSignals: true,
        onListening: () => {
            console.log(
                "[birdbox] Please wait for bundles to finish compiling."
            );
        },
    },
    plugins: [
        new RemoveEmptyScriptsPlugin(),
        new MiniCssExtractPlugin({
            filename: ({ chunk }) => `css/${chunk.name}.css`,
        }),
    ],
};
