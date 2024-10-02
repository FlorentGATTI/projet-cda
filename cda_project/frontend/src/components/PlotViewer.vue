<template>
  <div class="plot-viewer">
    <div class="trend-section">
      <div class="name-input">
        <v-select v-model="selectedName1" :items="filteredNames" :loading="loadingNames" @update:search-input="fetchFilteredNames" label="Sélectionnez le premier prénom" solo hide-details class="name-select" placeholder="Recherchez ou sélectionnez un prénom" searchable></v-select>
        <v-select v-model="selectedName2" :items="availableNames" label="Sélectionnez le deuxième prénom (facultatif)" solo hide-details class="name-select" placeholder="Recherchez ou sélectionnez un prénom" searchable v-if="availableNames.length"></v-select>
      </div>
      <button @click="fetchTrends" class="secondary-button">Générer un graphique de tendances</button>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <v-progress-circular v-if="loading" :size="70" :width="7" indeterminate color="primary" class="spinner"></v-progress-circular>

    <div id="plotly-chart" ref="plotlyChart" class="plot-container"></div>
  </div>
</template>

<script>
import Plotly from "plotly.js-dist";
import _ from "lodash";  // Pour utiliser la fonction debounce

const cachedData = {};

export default {
  data() {
    return {
      selectedName1: null,
      selectedName2: null,
      availableNames: [],
      filteredNames: [],
      loadingNames: false,
      errorMessage: "",
      loading: false,
    };
  },
  mounted() {
    this.fetchAvailableNames();  // Appeler ici pour charger les noms après que le composant soit monté
  },
  methods: {
    async fetchAvailableNames() {
      try {
        const response = await fetch("http://localhost:8000/api/names");
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.availableNames = data;
        this.filteredNames = data; // Initialiser filteredNames pour le second v-select
      } catch (error) {
        console.error("Erreur lors de la récupération des prénoms disponibles:", error);
        this.errorMessage = "Impossible de charger les prénoms disponibles.";
      }
    },

    fetchFilteredNames: _.debounce(async function(query) {
      if (!query) {
        this.filteredNames = [];
        return;
      }
      this.loadingNames = true;
      try {
        const response = await fetch(`http://localhost:8000/api/names?query=${encodeURIComponent(query)}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        this.filteredNames = data;
      } catch (error) {
        console.error("Erreur lors de la récupération des prénoms disponibles:", error);
      } finally {
        this.loadingNames = false;
      }
    }, 300), // Retarde l'exécution de la recherche de 300 ms

    async fetchTrends() {
      this.errorMessage = "";
      this.loading = true;

      try {
        const names = [this.selectedName1, this.selectedName2].filter((name) => name).join(",");

        if (!names) {
          throw new Error("Veuillez sélectionner au moins un prénom.");
        }

        const cacheKey = names;
        if (cachedData[cacheKey]) {
          this.renderPlot(cachedData[cacheKey]);
          return;
        }

        const url = `http://localhost:8000/api/plots/trends?names=${encodeURIComponent(names)}`;
        const response = await fetch(url);

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.detail || "Erreur inconnue lors de la génération du graphique.");
        }

        const data = await response.json();
        console.log("API Response Data:", data);
        cachedData[cacheKey] = data.figure;
        this.renderPlot(data.figure);
      } catch (error) {
        console.error("Erreur lors de la récupération des données:", error);
        this.errorMessage = error.message;
      } finally {
        this.loading = false;
      }
    },

    renderPlot(figureData) {
      const plotlyChart = this.$refs.plotlyChart;
      if (plotlyChart) {
        try {
          Plotly.react(plotlyChart, figureData.data, figureData.layout);
        } catch (error) {
          console.error("Error rendering plot:", error);
          this.errorMessage = "Erreur lors de l'affichage du graphique.";
        }
      } else {
        console.error("Plot container not found");
        this.errorMessage = "Erreur lors de l'affichage du graphique.";
      }
    },
  },
};
</script>

<style scoped>
.plot-viewer {
  text-align: center;
}

.trend-section {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.name-select {
  width: 300px;
  margin-bottom: 10px;
}

.error-message {
  color: #a26769;
  margin-top: 20px;
  font-weight: bold;
}

.secondary-button {
  margin: 5px;
}

.plot-container {
  max-width: 100%;
  display: flex;
  justify-content: center;
}

.spinner {
  margin-top: 20px;
}

.name-input {
  display: flex;
  gap: 20px;
}

@media (max-width: 1280px) {
  .name-input {
    flex-direction: column;
    gap: 5px;
  }
}
</style>
