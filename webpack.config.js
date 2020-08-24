const path = require('path')
const HTMLWebpackPlugin = require('html-webpack-plugin')
const {CleanWebpackPlugin} = require('clean-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const webpack = require('webpack')
const os = require('os')
const ifaces = os.networkInterfaces()
const hostIp = ifaces['eth0'][0].address

module.exports = {
    context: path.resolve(__dirname,'src'),
    mode: 'development',
    entry: './index.js',
    output: {
        publicPath: '/',
        filename: '[name].[hash].js',
        path: path.resolve(__dirname, 'app/static')
    },
    optimization: {
        splitChunks: {
            chunks: 'all'
        }
    },
    plugins: [
        new HTMLWebpackPlugin({
            template: './index.html',
            filename: path.resolve(__dirname, 'app/templates/index.html')
        }),
        new CleanWebpackPlugin({
            verbose: true
        }),
        new MiniCssExtractPlugin({
            filename: '[name].[hash].css'
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.$': 'jquery',
            'window.jQuery': 'jquery'
        })
    ],
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: "babel-loader",
                exclude: "/node_modules/"
            },
            {
                test: /\.css$/,
                use: [
                    // 'style-loader',
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    {
                        loader: 'postcss-loader',
                        options: {
                            sourceMap: true,
                            config: { path: 'src/postcss.config.js' }
                        }
                    }
                ]
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: './fonts'
                }
            },
            {
                test: /\.(png|jpg|gif)$/,
                loader: 'file-loader',
                options: {
                    name: '[name].[ext]',
                    outputPath: 'images'
                }
            },

        ]
    },
    devServer: {
        host: hostIp,
        port: 4200,
    }
}