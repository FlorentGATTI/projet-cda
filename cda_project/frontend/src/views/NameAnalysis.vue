<template>
  <div id="app">
    <h1>Analyse des Prénoms des Bébés aux États-Unis</h1>

    <div class="main-content">
      <div class="year-births-section">
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <div class="year-selector-wrapper">
                <label for="year">Sélectionnez une année :</label>
                <v-select
                  id="year"
                  v-model="selectedYear"
                  :items="years"
                  label="Veuillez sélectionner une année"
                  outlined
                  dense
                  style="width: 100%;"
                ></v-select>
              </div>
            </v-col>
            <v-col cols="12" md="6" v-if="totalBirths !== 0">
              <p>Total des naissances en {{ selectedYear }} : <span>{{ totalBirths }}</span></p>
              <p>Naissances masculines : <span>{{ birthsBySex?.M || 0 }}</span></p>
              <p>Naissances féminines : <span>{{ birthsBySex?.F || 0 }}</span></p>
            </v-col>
          </v-row>
        </v-container>
      </div>

      <div class="plot-section">
        <PlotViewer ref="plotViewer" />
      </div>
    </div>
  </div>
</template>

<script>
import PlotViewer from '../components/PlotViewer.vue';

export default {
  name: 'NameAnalysis',
  components: {
    PlotViewer
  },
  data() {
    return {
      years: Array.from({ length: 2021 - 1880 + 1 }, (v, k) => 1880 + k),
      selectedYear: null, 
      totalBirths: 0,
      birthsBySex: { M: 0, F: 0 },
    };
  },
  watch: {
    selectedYear() {
      this.fetchTotalBirths();
    }
  },
  methods: {
    async fetchTotalBirths() {
  if (!this.selectedYear) return;
  try {
    const response = await fetch(`http://127.0.0.1:8000/api/total_births/${this.selectedYear}`);
    const data = await response.json();
    this.totalBirths = data.total_births;
    this.birthsBySex = data.births_by_sex || { M: 0, F: 0 };
  } catch (error) {
    console.error('Erreur lors de la récupération du nombre total de naissances :', error);
  }
}
  },
  mounted() {
    this.fetchTotalBirths();
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  color: #0B4678; /* Indigo Dye */
  margin-top: 40px;
  font-family: 'Roboto', sans-serif;
}

h1 {
  color: #1976D2; /* Blue */
  font-size: 2.5em;
  margin-bottom: 20px;
}

.main-content {
  background: #E1D7CD; /* Light Beige */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: auto;
}

.year-births-section {
  background: transparent; /* Retire le fond moche */
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: none !important; /* Supprime toute ombre appliquée */
  border: none !important; /* Supprime toute bordure */
}

.year-selector-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
  background-color: transparent !important; /* Assurez-vous que l'arrière-plan est transparent */
  box-shadow: none !important; /* Supprime toute ombre qui pourrait apparaître */
  border: none !important; /* Supprime toute bordure */
}

.year-selector-wrapper label {
  font-size: 1.2em;
  margin-bottom: 10px;
}

v-select {
  background-color: transparent !important; /* Assurez-vous que le composant n'a pas de fond */
  box-shadow: none !important; /* Supprime toute ombre appliquée */
  border: none !important; /* Supprime toute bordure */
}

.v-input__control {
  background-color: transparent !important; /* Supprime le fond derrière l'input */
  box-shadow: none !important;
  border: none !important;
}

.v-select__slot, .v-select__selections {
  background-color: transparent !important; /* Supprime le fond à l'intérieur du slot */
  border: none !important;
}

.year-births-section p {
  font-size: 1.2em;
  margin: 0;
  text-align: right;
}

.year-births-section span {
  font-weight: bold;
  color: #6D2E46; /* Dark Pink */
}

.plot-section {
  background: #CDC1B5; /* Beige */
  padding: 20px;
  border-radius: 8px;
  max-width: 100%;
  overflow-x: auto; /* Assure que le graphique ne déborde pas horizontalement */
}
</style>