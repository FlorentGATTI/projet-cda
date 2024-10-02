<template>
  <v-container fluid>
    <h1 class="text-center main-title">Statistiques Globales</h1>

    <v-row>
      <v-col v-for="(analysis, index) in analyses" :key="index" :cols="12" :md="expandedCard === index ? 12 : 6" :lg="expandedCard === index ? 12 : 6">
        <v-card class="analysis-card" :class="{ 'expanded-card': expandedCard === index }" @click="expandCard(index)">
          <v-card-title class="card-title">
            <v-icon class="card-icon">{{ analysis.icon }}</v-icon>
            {{ analysis.title }}
          </v-card-title>
          <v-card-text class="card-text">
            {{ analysis.description }}
          </v-card-text>
          <v-card-actions v-if="expandedCard !== index">
            <v-btn color="primary" class="generate-btn">Générer</v-btn>
          </v-card-actions>
          <div v-if="expandedCard === index" class="plot-container" :id="`plot-container-${index}`"></div>
          <v-progress-circular v-if="loading && expandedCard === index" :size="50" :width="5" indeterminate color="primary" class="spinner"></v-progress-circular>
        </v-card>
      </v-col>
    </v-row>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  </v-container>
</template>

<script>
import Plotly from "plotly.js-dist";

const API_BASE_URL = "http://localhost:8000";

export default {
  name: "GlobalStat",
  data() {
    return {
      analyses: [
        {
          title: "Graphique de Diversité",
          description: "Analysez la diversité des prénoms au cours des années.",
          icon: "mdi-chart-bar",
          fetchMethod: "fetchDiversity",
        },
        {
          title: "Tracé de Longueur de Nom",
          description: "Visualisez la longueur des prénoms à travers différentes périodes.",
          icon: "mdi-ruler",
          fetchMethod: "fetchNameLength",
        },
        {
          title: "Analyse par Décennie",
          description: "Obtenez une analyse des prénoms par décennie.",
          icon: "mdi-calendar-clock",
          fetchMethod: "fetchDecadeAnalysis",
        },
      ],
      selectedYear: null,
      years: Array.from({ length: 2021 - 1880 + 1 }, (v, k) => 1880 + k),
      totalBirths: 0,
      birthsBySex: { M: 0, F: 0 },
      errorMessage: "",
      loading: false,
      plotImage: null,
      expandedCard: null,
    };
  },
  watch: {
    selectedYear() {
      this.fetchTotalBirths();
    },
  },
  methods: {
    expandCard(index) {
      if (this.expandedCard === index) {
        this.expandedCard = null;
        this.plotImage = null;
      } else {
        this.expandedCard = index;
        this[this.analyses[index].fetchMethod]();
      }
    },

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

    async handlePlotRequest(url) {
      this.errorMessage = "";
      this.loading = true;
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.figure) {
          const figureData = JSON.parse(data.figure);
          this.renderPlotlyPlot(figureData);
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
      const plotContainer = document.getElementById(`plot-container-${this.expandedCard}`);
      if (!plotContainer) {
        console.error('Plot container not found');
        return;
      }
      
      const layout = {
        ...figureData.layout,
        width: plotContainer.offsetWidth,
        height: 400,
        margin: { l: 50, r: 50, t: 50, b: 50 },
      };
      
      Plotly.newPlot(plotContainer, figureData.data, layout, { responsive: true });
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
  },
  mounted() {
    this.fetchTotalBirths();
  },
};
</script>

<style scoped>
.analysis-card {
  margin: 20px;
  padding: 15px;
  transition: box-shadow 0.3s, transform 0.3s, all 0.5s ease-in-out;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-radius: 10px;
  cursor: pointer;
  min-width: 450px;
  min-height: 220px;
  height: 200px;
}

.analysis-card.expanded-card {
  transform: scale(1.05);
  padding: 25px;
  height: auto;
}

.card-title {
  font-size: 1.4em;
  font-weight: bold;
  color: #333;
  display: flex;
  align-items: center;
}

.card-icon {
  margin-right: 10px;
  font-size: 2em;
  color: #004ba0;
}

.card-text {
  font-size: 1em;
  color: #555;
}

.generate-btn {
  width: 100%;
  text-transform: uppercase;
  font-weight: bold;
  transition: background-color 0.3s, transform 0.3s;
  border-radius: 8px;
}

.generate-btn:hover {
  background-color: #004ba0;
  transform: scale(1.05);
}

.plot-container {
  max-width: 100%;
  height: auto;
  margin-top: 20px;
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
  display: flex;
  justify-content: center;
}

.total-births-section {
  margin-top: 30px;
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

.error-message {
  color: #ff6f61;
  margin-top: 20px;
  font-weight: bold;
  text-align: center;
}
</style>