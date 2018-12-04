const webpack = require('webpack')

// module.exports = {
//     module: {
//         rules: [{
//             test: /\.js$/,
//             exclude: /node_modules/,
//             use: {
//                 loader: "babel-loader"
//             }
//         }]
//     }
// };

module.exports = (env) => {
    // https://medium.com/@trekinbami/using-environment-variables-in-react-6b0a99d83cf5
    const envKeys = Object.keys(env).reduce((prev, next) => {
        prev[`process.env.${next}`] = JSON.stringify(env[next]);
        return prev;
    }, {});

    const path = require('path');
    return {
        entry: {
            cafeList: './src/frontend/assets/cafe-list.app.js',
            cafeDetail: './src/frontend/assets/cafe-detail.app.js',
        },
        output: {
            path: path.resolve(__dirname, 'src/frontend/static/frontend/'),
            filename: "[name].js"
        },
        module: {

            rules: [{
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }, {
                test: /\.(sass|scss)$/,
                use: [{
                    loader: "style-loader"
                }, {
                    loader: "css-loader"
                }, {
                    loader: "sass-loader"
                }]
            }]
        },
        plugins: [
            new webpack.DefinePlugin(envKeys)
        ]
    };
};
