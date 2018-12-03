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

    return {
        module: {
            rules: [{
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader"
                }
            }]
        },
        plugins: [
            new webpack.DefinePlugin(envKeys)
        ]
    };
};
