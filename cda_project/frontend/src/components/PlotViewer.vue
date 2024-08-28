<template>
  <div class="plot-viewer">
    <div class="trend-section">
      <input class="name-input" v-model="names" placeholder="Entrez les prénoms séparés par des virgules" />
      <button @click="fetchTrends">Générer un graphique de tendances</button>
    </div>
    <div class="buttons">
      <button @click="fetchDiversity">Générer un graphique de diversité</button>
      <button @click="fetchNameLength">Générer un tracé de longueur de nom</button>
      <button @click="fetchDecadeAnalysis">Générer une analyse par décennie</button>
      <button @click="fetchGeographicDiversity">Générer une analyse de diversité géographique</button>
      <button @click="fetchCompoundNames">Générer une analyse des prénoms composés</button>
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <img :src="plotImage" alt="Generated Plot" v-if="plotImage && !errorMessage" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      names: '',
      plotImage: '',
      errorMessage: ''
    };
  },
  methods: {
    async fetchTrends() {
      this.errorMessage = '';
      this.plotImage = ''; // Clear the previous image
      try {
        if (!this.names) {
          throw new Error('Veuillez entrer au moins un prénom.');
        }
        const response = await fetch(`http://localhost:8000/api/plots/trends?names=${encodeURIComponent(this.names)}`);
        const data = await response.json();
        console.log('Trends plot data received:', data);
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || 'Erreur inconnue');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async fetchDiversity() {
      this.errorMessage = '';
      this.plotImage = ''; // Clear the previous image
      try {
        console.log('Fetching diversity');
        const response = await fetch('http://localhost:8000/api/plots/diversity');
        const data = await response.json();
        console.log('Diversity plot data received:', data);
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || 'Erreur inconnue');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async fetchNameLength() {
      this.errorMessage = '';
      this.plotImage = ''; // Clear the previous image
      try {
        console.log('Fetching name length');
        const response = await fetch('http://localhost:8000/api/plots/name_length');
        const data = await response.json();
        console.log('Name length plot data received:', data);
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || 'Erreur inconnue');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async fetchDecadeAnalysis() {
      this.errorMessage = '';
      this.plotImage = '';
      try {
        console.log('Fetching decade analysis');
        const response = await fetch('http://localhost:8000/api/plots/decade_analysis');
        const data = await response.json();
        console.log('Decade analysis plot data received:', data);
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || 'Erreur inconnue');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async fetchGeographicDiversity() {
      this.errorMessage = '';
      this.plotImage = '';
      try {
        console.log('Fetching geographic diversity');
        const response = await fetch('http://localhost:8000/api/plots/geographic_diversity');
        const data = await response.json();
        console.log('Geographic diversity plot data received:', data);
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || 'Erreur inconnue');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    },
    async fetchCompoundNames() {
      this.errorMessage = '';
      this.plotImage = '';
      try {
        console.log('Fetching compound names analysis');
        const response = await fetch('http://localhost:8000/api/plots/compound_names');
        const data = await response.json();
        console.log('Compound names plot data received:', data);
        if (response.ok) {
          this.plotImage = `data:image/png;base64,${data.image}`;
        } else {
          throw new Error(data.detail || 'Erreur inconnue');
        }
      } catch (error) {
        this.errorMessage = error.message;
      }
    }
  }
};
</script>

<style scoped>
.plot-viewer {
  text-align: center;
}

.trend-section, .buttons {
  margin: 20px 0;
}

.name-input {
  width: 300px; /* Adjust the width as needed */
  padding: 8px;
  font-size: 1em;
}

.error-message {
  color: red;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  margin: 5px;
  font-size: 1em;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #135ba1;
}
</style>