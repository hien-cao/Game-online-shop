module.exports = {
  entry: './src/index.js',
  output: {
    filename: './static/scripts/bundle.js',
  },
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: 'node_modules',
        use: 'babel-loader',
      },
    ],
  },
};
