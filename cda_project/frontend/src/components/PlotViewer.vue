<template>
  <div class="plot-viewer">
    <div class="trend-section">
      <div class="name-input">
        <v-select v-model="selectedName1" :items="availableNames" label="Sélectionnez le premier prénom" solo hide-details class="name-select" placeholder="Recherchez ou sélectionnez un prénom" searchable v-if="availableNames.length"></v-select>
        <v-select v-model="selectedName2" :items="availableNames" label="Sélectionnez le deuxième prénom (facultatif)" solo hide-details class="name-select" placeholder="Recherchez ou sélectionnez un prénom" searchable v-if="availableNames.length"></v-select>
      </div>
      <button @click="fetchTrends" class="secondary-button">Générer un graphique de tendances</button>

    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <v-progress-circular
      v-if="loading"
      :size="70"
      :width="7"
      indeterminate
      color="primary"
      class="spinner"
    ></v-progress-circular>

    <div id="plotly-chart" ref="plotlyChart" class="plot-container"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist'

export default {
  data() {
    return {
      selectedName1: null,
      selectedName2: null,
      availableNames: [],
      errorMessage: "",
      loading: false,
    };
  },
  created() {
    this.fetchAvailableNames();
  },
  methods: {
    async fetchAvailableNames() {
      try {
        const response = await fetch('http://localhost:8000/api/names');
        const data = await response.json();
        this.availableNames = data;
      } catch (error) {
        console.error("Erreur lors de la récupération des prénoms disponibles:", error);
        this.errorMessage = "Impossible de charger les prénoms disponibles.";
      }
    },

  async fetchTrends() {
  this.errorMessage = "";
  this.loading = true;

  try {
    const names = [this.selectedName1, this.selectedName2]
      .filter(name => name)
      .join(',');
    
    if (!names) {
      throw new Error("Veuillez sélectionner au moins un prénom.");
    }

    const url = `http://localhost:8000/api/plots/trends?names=${encodeURIComponent(names)}`;
    const response = await fetch(url);
    const data = await response.json();

    if (response.ok) {
      console.log("API Response Data:", data);
      this.renderPlot(data.figure);
    } else {
      throw new Error(data.detail || "Erreur inconnue lors de la génération du graphique.");
    }
  } catch (error) {
    this.errorMessage = error.message;
  } finally {
    this.loading = false;
  }
},

    async handlePlotRequest(plotType) {
      this.errorMessage = "";
      this.loading = true;

      try {
        let url = `http://localhost:8000/api/plots/${plotType}`;
        if (plotType === 'trends') {
          const queryParams = new URLSearchParams();
          if (this.selectedName1) queryParams.append("name1", this.selectedName1);
          if (this.selectedName2) queryParams.append("name2", this.selectedName2);
          url += `?${queryParams.toString()}`;
        }

        const response = await fetch(url);
        const data = await response.json();

        if (response.ok) {
          console.log("API Response Data:", data);
          this.renderPlot(data.figure);
        } else {
          throw new Error(data.detail || "Erreur inconnue lors de la génération du graphique.");
        }
      } catch (error) {
        this.errorMessage = error.message;
      } finally {
        this.loading = false;
      }
    },

    renderPlot(figureData) {
  const plotlyChart = this.$refs.plotlyChart;
  if (plotlyChart) {
    try {
      // Check if figureData is already an object
      const plotData = typeof figureData === 'string' ? JSON.parse(figureData) : figureData;
      Plotly.newPlot(plotlyChart, plotData);
    } catch (error) {
      console.error('Error rendering plot:', error);
      this.errorMessage = "Erreur lors de l'affichage du graphique.";
    }
  } else {
    console.error('Plot container not found');
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

.buttons {
  margin: 20px 0;
}

.name-select {
  width: 300px;
  margin-bottom: 10px;
}

.trend-button {
  margin-top: 10px;
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
  /* height: 600px; */
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
