<template>
  <div class="plot-viewer">
    <div class="trend-section">
      <!-- Sélecteur pour le premier prénom -->
      <v-select
        v-model="selectedName1"
        :items="availableNames"
        label="Sélectionnez le premier prénom"
        solo
        hide-details
        class="name-select"
        placeholder="Recherchez ou sélectionnez un prénom"
        searchable
        v-if="availableNames.length"
      ></v-select>

      <!-- Sélecteur pour le deuxième prénom -->
      <v-select
        v-model="selectedName2"
        :items="availableNames"
        label="Sélectionnez le deuxième prénom (facultatif)"
        solo
        hide-details
        class="name-select"
        placeholder="Recherchez ou sélectionnez un prénom"
        searchable
        v-if="availableNames.length"
      ></v-select>

      <!-- Bouton pour générer le graphique de tendances -->
      <v-btn color="primary" @click="fetchTrends" class="trend-button">Générer un graphique de tendances</v-btn>
    </div>

    <!-- Boutons pour d'autres analyses -->
    <div class="buttons">
      <button @click="fetchDiversity" class="secondary-button">Générer un graphique de diversité</button>
      <button @click="fetchNameLength" class="secondary-button">Générer un tracé de longueur de nom</button>
      <button @click="fetchDecadeAnalysis" class="secondary-button">Générer une analyse par décennie</button>
      <button @click="fetchGeographicDiversity" class="secondary-button">Générer une analyse de diversité géographique</button>
      <button @click="fetchCompoundNames" class="secondary-button">Générer une analyse des prénoms composés</button>
    </div>

    <!-- Affichage des messages d'erreur -->
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <!-- Conteneur pour afficher le graphique -->
    <div class="plot-container">
      <img :src="plotImage" alt="Generated Plot" v-if="plotImage && !errorMessage" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedName1: null, // Stocke le prénom sélectionné 1
      selectedName2: null, // Stocke le prénom sélectionné 2
      availableNames: [], // Stocke la liste des prénoms disponibles
      plotImage: "", // Stocke l'image du graphique
      errorMessage: "", // Stocke les messages d'erreur
    };
  },
  created() {
    this.fetchAvailableNames(); // Charger les noms disponibles au montage du composant
  },
  methods: {
    // Méthode pour récupérer la liste des prénoms disponibles depuis l'API
    async fetchAvailableNames() {
      try {
        const response = await fetch('http://localhost:8000/api/names');
        const data = await response.json();
        this.availableNames = data; // Assigne les prénoms disponibles à la variable
      } catch (error) {
        console.error("Erreur lors de la récupération des prénoms disponibles:", error);
        this.errorMessage = "Impossible de charger les prénoms disponibles.";
      }
    },

    // Méthode pour générer le graphique de tendances
    async fetchTrends() {
      this.errorMessage = "";
      this.plotImage = ""; // Efface l'image précédente

      // Vérification que le premier prénom est sélectionné
      if (!this.selectedName1) {
        this.errorMessage = "Veuillez sélectionner au moins un prénom.";
        return;
      }

      try {
        const queryParams = new URLSearchParams();
        if (this.selectedName1) queryParams.append("name1", this.selectedName1);
        if (this.selectedName2) queryParams.append("name2", this.selectedName2);

        const response = await fetch(`http://localhost:8000/api/plots/trends?${queryParams.toString()}`);
        const data = await response.json();

        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || "Erreur inconnue lors de la génération du graphique.");
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },

    // Autres méthodes pour générer les différents graphiques
    async fetchDiversity() {
      this.handlePlotRequest("http://localhost:8000/api/plots/diversity");
    },
    async fetchNameLength() {
      this.handlePlotRequest("http://localhost:8000/api/plots/name_length");
    },
    async fetchDecadeAnalysis() {
      this.handlePlotRequest("http://localhost:8000/api/plots/decade_analysis");
    },
    async fetchGeographicDiversity() {
      this.handlePlotRequest("http://localhost:8000/api/plots/geographic_diversity");
    },
    async fetchCompoundNames() {
      this.handlePlotRequest("http://localhost:8000/api/plots/compound_names");
    },

    // Méthode générique pour gérer les requêtes de graphique
    async handlePlotRequest(url) {
      this.errorMessage = "";
      this.plotImage = ""; // Clear the previous image
      try {
        const response = await fetch(url);
        const data = await response.json();
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || "Erreur inconnue lors de la génération du graphique.");
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
  },
};
</script>

<style scoped>
.plot-viewer {
  text-align: center;
  background: #cdc1b5; /* Beige */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  max-width: 100%;
}

.trend-section {
  margin: 20px 0;
  display: flex;
  flex-direction: column;
  align-items: center; /* Centrer les éléments horizontalement */
}

.buttons {
  margin: 20px 0;
}

.name-select {
  width: 300px;
  margin-bottom: 10px;
}

.trend-button {
  margin-top: 10px; /* Ajoute un peu d'espace en haut */
}

.error-message {
  color: #a26769; /* Brun-rosé */
  margin-top: 20px;
  font-weight: bold;
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
</style>
