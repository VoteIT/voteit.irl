const path = require("path");

module.exports = {
  outputDir: path.resolve(__dirname, "../voteit/irl/static/vue"),
  configureWebpack: {
    resolve: {
      alias: {
        'src': path.resolve(__dirname, 'src'),
        'assets': path.resolve(__dirname, 'src/assets'),
        'components': path.resolve(__dirname, 'src/components')
      }
    }
  }
}
