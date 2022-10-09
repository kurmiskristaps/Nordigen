const path = require('path');

module.exports = {
  entry: './assets/index.js',
  output: {
    filename: 'index-bundle.js',
    path: path.resolve(__dirname, './static'),
  },
};
