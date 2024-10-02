<template>
  <v-container fluid>
    <h1 class="text-center main-title">Statistiques Globales</h1>
    
    <div class="buttons">
      <button @click="fetchDiversity" class="secondary-button">Générer un graphique de diversité</button>
      <button @click="fetchNameLength" class="secondary-button">Générer un tracé de longueur de nom</button>
      <button @click="fetchDecadeAnalysis" class="secondary-button">Générer une analyse par décennie</button>
      <button @click="fetchGeographicDiversity" class="secondary-button">Générer une analyse de diversité géographique</button>
      <button @click="fetchCompoundNames" class="secondary-button">Générer une analyse des prénoms composés</button>
    </div>

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

    <div class="graph-container">
      <div class="plot-container" v-if="!loading">
        <img :src="plotImage" alt="Generated Plot" v-if="plotImage && !errorMessage" />
      </div>
    </div>

    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <v-progress-circular v-if="loading" :size="70" :width="7" indeterminate color="primary" class="spinner"></v-progress-circular>
  </v-container>
</template>

<script>
import Plotly from "plotly.js-dist";

const API_BASE_URL = "http://localhost:8000";

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
      plotImage: null,
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
        const response = await fetch(`${API_BASE_URL}/api/total_births/${this.selectedYear}`, {
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
      } finally {
        this.loading = false;
      }
    },

    async fetchYearlyBirths() {
      await this.handlePlotRequest(`${API_BASE_URL}/api/plots/yearly_births`);
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
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else if (data.figure) {
          this.renderPlotlyPlot(JSON.parse(data.figure));
        } else {
          throw new Error("Format de données non reconnu.");
        }
      } catch (error) {
        console.error("Erreur lors de la génération du graphique:", error);
        this.errorMessage = error.message || "Erreur inconnue lors de la génération du graphique.";
      } finally {
        this.loading = false;
      }
    },

    renderPlotlyPlot(figureData) {
      const plotlyChart = this.$refs.plotlyChart;
      if (plotlyChart) {
        const layout = {
          ...figureData.layout,
          width: plotlyChart.offsetWidth,
          height: 500,
          margin: { l: 50, r: 50, t: 50, b: 50 },
        };
        Plotly.newPlot(plotlyChart, figureData.data, layout, { responsive: true });
      } else {
        console.error("Plot container not found");
        this.errorMessage = "Erreur lors de l'affichage du graphique.";
      }
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

.buttons {
  margin-top: 20px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.error-message {
  color: #a26769;
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
  color: #6d2e46;
}
</style>
