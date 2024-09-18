import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import './assets/app.css';

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        primary: '#1976D2',   // Blue
        secondary: '#A26769', // Brownish-pink
        accent: '#6D2E46',    // Dark pink
        background: '#E1D7CD', // Light beige
        surface: '#CDC1B5',   // Beige
        error: '#FF5252',
        info: '#2196F3',
        success: '#4CAF50',
        warning: '#FB8C00',
      },
    },
  },
})

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')
