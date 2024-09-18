const { defineConfig } = require('@vue/cli-service')
const webpack = require('webpack');

module.exports = defineConfig({
  transpileDependencies: ['vuetify'],
  outputDir: '../app/static',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_OPTIONS_API__: true,
        __VUE_PROD_DEVTOOLS__: false,
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
      })
    ]
  }
})
