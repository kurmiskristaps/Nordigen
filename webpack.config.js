const path = require('path');

module.exports = {
  entry: './assets/accounts.js',
  output: {
    filename: 'accounts.js',
    path: path.resolve(__dirname, './static'),
  },
};
