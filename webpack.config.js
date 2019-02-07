const path = require('path');

module.exports = {
  entry: {
    core: './src/index.js',
    game: './src/games/play.js',
    review: './src/review.js',
    search: './src/search.js',
    profile: './src/profile.js',
  },
  output: {
    path: path.resolve(__dirname, 'apps', 'core', 'static', 'scripts'),
    filename: '[name].js',
  },
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.m?js$/,
        exclude: /(node_modules)/,
        use: 'babel-loader',
      },
    ],
  },
};
