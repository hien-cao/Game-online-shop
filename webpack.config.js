module.exports = {
  entry: {
    core: './src/index.js',
    game: './src/games/play.js',
  },
  output: {
    filename: './static/scripts/[name].js',
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
