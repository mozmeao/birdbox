/*
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 */

'use strict';

const CopyPlugin = require('copy-webpack-plugin');
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'birdbox/birdbox/static/'),
        publicPath: '/src/'
    },
    performance: {
        hints: 'warning'
    },
    plugins: [
        // Clean out /static before processing
        new CleanWebpackPlugin(),
        new CopyPlugin({
            patterns: [
                {
                    // Copy Protocol images to /static.
                    from: path.resolve(
                        __dirname,
                        'node_modules/@mozilla-protocol/core/protocol/img/'
                    ),
                    to: 'protocol/img/'
                },
                {
                    // Copy Protocol fonts to /static.
                    from: path.resolve(
                        __dirname,
                        'node_modules/@mozilla-protocol/core/protocol/fonts/'
                    ),
                    to: 'protocol/fonts/'
                }
            ]
        })
    ]
};
