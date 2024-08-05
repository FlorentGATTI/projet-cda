const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  outputDir: '../app/static',
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
