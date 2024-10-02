<template>
  <v-container fluid>
    <h2>Statistiques Globales des Prénoms</h2>

    <!-- Year Selection -->
    <v-select
      v-model="selectedYear"
      :items="years"
      label="Sélectionnez l'année"
      solo
      hide-details
      class="year-select"
      placeholder="Recherchez ou sélectionnez une année"
      searchable
    ></v-select>
    <!-- <v-btn @click="generateYearlyBirthsGraph" class="primary-button">Générer le graphique</v-btn> -->


    <!-- Boutons pour d'autres analyses -->
    <div class="buttons">
      <button @click="fetchDiversity" class="secondary-button">Générer un graphique de diversité</button>
      <button @click="fetchNameLength" class="secondary-button">Générer un tracé de longueur de nom</button>
      <button @click="fetchDecadeAnalysis" class="secondary-button">Générer une analyse par décennie</button>
      <button @click="fetchGeographicDiversity" class="secondary-button">Générer une analyse de diversité géographique</button>
      <button @click="fetchCompoundNames" class="secondary-button">Générer une analyse des prénoms composés</button>
    </div>

    <!-- Display total births -->
    <div v-if="totalBirths !== 0" class="total-births-section">
      <p>
        Total des naissances en {{ selectedYear }} : <span>{{ totalBirths }}</span>
      </p>
      <p>
        Naissances masculines : <span>{{ birthsBySex?.M || 0 }}</span>
      </p>
      <p>
        Naissances féminines : <span>{{ birthsBySex?.F || 0 }}</span>
      </p>
    </div>

    <!-- Placeholder pour les graphiques interactifs -->
    <div class="graph-container">
      <div id="plotly-chart" ref="plotlyChart" class="graph-placeholder"></div>
    </div>

    <!-- Affichage des messages d'erreur -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- Spinner de chargement -->
    <v-progress-circular v-if="loading" :size="70" :width="7" indeterminate color="primary" class="spinner"></v-progress-circular>
  </v-container>
</template>

<script>
import Plotly from 'plotly.js-dist'

const API_BASE_URL = 'http://localhost:8000';

export default {
  name: "GlobalStat",
  data() {
    return {
      selectedYear: null,
      years: Array.from({ length: 2021 - 1880 + 1 }, (v, k) => 1880 + k),
      totalBirths: 0,
      birthsBySex: { M: 0, F: 0 },
      errorMessage: "",
      loading: false,
    };
  },
  watch: {
    selectedYear() {
      this.fetchTotalBirths();
    },
  },
  methods: {
    async fetchTotalBirths() {
      if (!this.selectedYear) return;
      this.loading = true;
      this.errorMessage = "";
      try {
        const response = await fetch(`${API_BASE_URL}/api/total_births/${this.selectedYear}`);
    // Méthode placeholder pour charger les données
    loadChartData() {
      console.log("Chargement des données pour les graphiques");
      // Logique pour charger les données (à remplir avec Plotly plus tard)
    },

    // Méthode pour récupérer le nombre total de naissances
    async fetchTotalBirths() {
      if (!this.selectedYear) return;
      this.errorMessage = "";
      try {
        const response = await fetch(`http://localhost:8000/api/total_births/${this.selectedYear}`, {
          credentials: "include",
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.totalBirths = data.total_births;
        this.birthsBySex = data.births_by_sex || { M: 0, F: 0 };
      } catch (error) {
          console.error("Erreur lors de la récupération du nombre total de naissances :", error);
        this.errorMessage = `Erreur lors de la récupération des données : ${error.message}`;
        this.totalBirths = 0;
        this.birthsBySex = { M: 0, F: 0 };
      }
    },

    // Méthode pour générer le graphique de naissances par année
    async fetchYearlyBirths() {
      this.errorMessage = "";
      this.loading = true; // Démarre le spinner de chargement
      try {
        const response = await fetch("http://localhost:8000/api/plots/yearly_births");
        const data = await response.json();
        if (response.ok) {
          console.log("Graph data fetched successfully:", data);
          this.renderPlot(data.image);
        } else {
          throw new Error(data.detail || "Erreur inconnue lors de la génération du graphique.");
        }
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false;
      }
    },

    async fetchDiversity() {
      await this.handlePlotRequest(`${API_BASE_URL}/api/plots/diversity`);
    },
    async fetchNameLength() {
      await this.handlePlotRequest(`${API_BASE_URL}/api/plots/name_length`);
    },
    async fetchDecadeAnalysis() {
      await this.handlePlotRequest(`${API_BASE_URL}/api/plots/decade_analysis`);
    },
    async fetchGeographicDiversity() {
      await this.handlePlotRequest(`${API_BASE_URL}/api/plots/geographic_diversity`);
    },
    async fetchCompoundNames() {
      await this.handlePlotRequest(`${API_BASE_URL}/api/plots/compound_names`);
    },

    async handlePlotRequest(url) {
      this.errorMessage = "";
      this.loading = true;
      try {
        const queryParams = new URLSearchParams();
        if (this.selectedYear) queryParams.append("year", this.selectedYear);

        const response = await fetch(`${url}?${queryParams.toString()}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.image) {
          this.renderImagePlot(data.image);
        } else if (data.figure) {
          this.renderPlotlyPlot(data.figure);
        } else {
          throw new Error("Format de données non reconnu.");
        }
      } catch (error) {
        console.error('Erreur lors de la génération du graphique:', error);
        this.errorMessage = error.message || "Erreur inconnue lors de la génération du graphique.";
      } finally {
        this.loading = false;
      }
    },

    renderImagePlot(imageBase64) {
      const plotlyChart = this.$refs.plotlyChart;
      if (plotlyChart) {
        const img = new Image();
        img.src = `data:image/png;base64,${imageBase64}`;
        img.onload = () => {
          Plotly.newPlot(plotlyChart, [{
            x: [0],
            y: [0],
            type: 'scatter',
            mode: 'markers',
            marker: {opacity: 0}
          }], {
            images: [{
              source: img.src,
              xref: "paper",
              yref: "paper",
              x: 0,
              y: 1,
              sizex: 1,
              sizey: 1,
              sizing: "stretch",
              layer: "below"
            }],
            xaxis: {visible: false},
            yaxis: {visible: false},
            width: plotlyChart.offsetWidth,
            height: plotlyChart.offsetHeight,
            margin: {l: 0, r: 0, t: 0, b: 0}
          }, {displayModeBar: false});
        };
      } else {
        console.error('Plot container not found');
        this.errorMessage = "Erreur lors de l'affichage du graphique.";
    // Méthode pour afficher le graphique avec Plotly
    renderPlot(imageBase64) {
      const plotContainer = document.getElementById("yearly-births-plot");
      if (plotContainer) {
        console.log("Rendering plot in container:", plotContainer);
        const img = new Image();
        img.src = `data:image/png;base64,${imageBase64}`;
        img.alt = "Generated Plot";
        plotContainer.innerHTML = ""; // Clear previous content
        plotContainer.appendChild(img);
      } else {
        console.error("Plot container not found");
      }
    },

    renderPlotlyPlot(figureData) {
      const plotlyChart = this.$refs.plotlyChart;
      if (plotlyChart) {
        const layout = {
          ...figureData.layout,
          width: plotlyChart.offsetWidth,
          height: 500, // You can adjust this value
          margin: { l: 50, r: 50, t: 50, b: 50 }
        };
        Plotly.newPlot(plotlyChart, figureData.data, layout, { responsive: true });
      } else {
        console.error('Plot container not found');
        this.errorMessage = "Erreur lors de l'affichage du graphique.";
      }
      await this.fetchYearlyBirths();
    },
  },
  mounted() {
    this.fetchTotalBirths();
  },
};
</script>

<style scoped>
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

.buttons {
  margin: 20px 0;
}

.secondary-button {
  background-color: #a26769; /* Brun-rosé */
  color: white;
  border: none;
  padding: 10px 15px;
  margin: 5px;
  cursor: pointer;
  font-size: 0.9em;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.secondary-button:hover {
  background-color: #6d2e46; /* Dark Pink */
}

.primary-button {
  background-color: #6d2e46; /* Dark Pink */
  color: white;
  border: none;
  padding: 10px 15px;
  margin: 5px;
  cursor: pointer;
  font-size: 0.9em;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.primary-button:hover {
  background-color: #a26769; /* Brun-rosé */
}

.error-message {
  color: #a26769; /* Brun-rosé */
  margin-top: 20px;
  font-weight: bold;
}

.plot-container {
  max-width: 100%;
  height: auto;
  display: flex;
  justify-content: center;
}

.plot-container img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
}

.spinner {
  margin-top: 20px;
}

.year-select {
  width: 300px;
  margin-bottom: 20px;
}

.total-births-section {
  margin-top: 20px;
  text-align: right;
}

.total-births-section p {
  font-size: 1.2em;
  margin: 0;
}

.total-births-section span {
  font-weight: bold;
  color: #6d2e46; /* Dark Pink */
}
</style>
