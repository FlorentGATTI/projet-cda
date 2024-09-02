<template>
    <div id="app">
      <h1>Statistiques Globales des Prénoms</h1>
      
      <!-- Placeholder pour les graphiques interactifs -->
      <div class="graph-container">
        <!-- Placeholder pour un graphique -->
        <div class="graph-placeholder">
          Graphique 1: Nombre de naissances par année (à intégrer avec Plotly)
        </div>
        <!-- Placeholder pour un autre graphique -->
        <div class="graph-placeholder">
          Graphique 2: Proportion des prénoms par année (à intégrer avec Plotly)
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'GlobalStat',
    data() {
      return {
        // On peut définir ici les données ou les options qui seront utilisées avec Plotly plus tard
        chartData: null,
        chartOptions: null,
      };
    },
    methods: {
      // Méthode placeholder pour charger les données
      loadChartData() {
        console.log('Chargement des données pour les graphiques');
        // Logique pour charger les données (à remplir avec Plotly plus tard)
      },
    },
    mounted() {
      this.loadChartData();
    },
  };
  </script>
  
  <style scoped>
  h1 {
    text-align: center;
  }
  .graph-container {
    margin-top: 20px;
  }
  
  .graph-placeholder {
    background-color: #f0f0f0;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 20px;
    text-align: center;
    margin-bottom: 20px;
  }
  </style>
  