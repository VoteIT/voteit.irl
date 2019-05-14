const path = require("path");

let outputDir = path.resolve(__dirname, "../voteit/irl/static/vue");

module.exports = {
  outputDir: outputDir,
  configureWebpack: {
    output: {
      filename: "js/bundle.js",
      chunkFilename: "js/vendor_chunks.js"
      //filename: outputDir + "hej.js",
      //chunkFilename: outputDir + "/hej.js"
    },
    resolve: {
      alias: {
        'src': path.resolve(__dirname, 'src'),
        'assets': path.resolve(__dirname, 'src/assets'),
        'components': path.resolve(__dirname, 'src/components'),
        'arche': path.resolve(__dirname, 'src/arche')
      }
    }
  },
  chainWebpack: config => {
    if (config.plugins.has("extract-css")) {
      const extractCSSPlugin = config.plugin("extract-css");
      extractCSSPlugin &&
        extractCSSPlugin.tap(() => [
          {
            filename: "css/bundle.css",
            chunkFilename: "css/vendor_chunks.css"
          }
        ]);
    }
  }
}
