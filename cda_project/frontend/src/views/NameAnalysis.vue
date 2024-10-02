<template>
  <div id="app">
    <h1>Analyse des Prénoms des Bébés aux États-Unis</h1>

    <div class="main-content">
      <div class="year-births-section">
        <v-container>
          <p v-if="selectedYearEnd">Nombre total de naissance compris entre {{ selectedYearStart }} et {{ selectedYearEnd }} : {{ formatNumber(calculateTotalBirths()) }}</p>
          <v-row>
            <!-- Premier v-select pour sélectionner la première année -->
            <v-col cols="12" md="6">
              <div class="year-selector-wrapper">
                <label for="year-start">Sélectionnez une année de début :</label>
                <v-select
                  id="year-start"
                  v-model="selectedYearStart"
                  :items="years"
                  label="Veuillez sélectionner une année de début"
                  outlined
                  dense
                  style="width: 100%;"
                ></v-select>
              </div>
            </v-col>

            <!-- Deuxième v-select pour sélectionner la deuxième année -->
            <v-col cols="12" md="6" v-if="selectedYearStart">
              <div class="year-selector-wrapper">
                <label for="year-end">Sélectionnez une année de fin :</label>
                <v-select
                  id="year-end"
                  v-model="selectedYearEnd"
                  :items="years"
                  label="Veuillez sélectionner une année de fin"
                  outlined
                  dense
                  style="width: 100%;"
                ></v-select>
              </div>
            </v-col>

            <v-col cols="12" v-if="birthData.length > 0">
              <div class="births-table-wrapper">
                <table class="births-table">
                  <thead>
                    <tr>
                      <th>Année</th>
                      <th>Total des Naissances</th>
                      <th>Naissances Masculines</th>
                      <th>Naissances Féminines</th>
                      <th>% Masculin</th>
                      <th>% Féminin</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="data in birthData" :key="data.year">
                      <td>{{ data.year }}</td>
                      <td>{{ formatNumber(data.total_births) }}</td>
                      <td>{{ formatNumber(data.male_births) }}</td>
                      <td>{{ formatNumber(data.female_births) }}</td>
                      <td>{{ ((data.male_births / data.total_births) * 100).toFixed(2) }}%</td>
                      <td>{{ ((data.female_births / data.total_births) * 100).toFixed(2) }}%</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </div>
    </div>

    <div class="plot-section">
      <PlotViewer ref="plotViewer" />
    </div>
  </div>
</template>

<script>
import PlotViewer from '../components/PlotViewer.vue';

export default {
  name: 'NameAnalysis',
  components: {
    PlotViewer,
  },
  data() {
    return {
      years: Array.from({ length: 2021 - 1880 + 1 }, (v, k) => 1880 + k),
      selectedYearStart: null,
      selectedYearEnd: null,
      birthData: [],
    };
  },
  watch: {
    selectedYearStart() {
      this.fetchTotalBirths();
    },
    selectedYearEnd() {
      this.fetchTotalBirths();
    },
  },
  methods: {
    async fetchTotalBirths() {
      if (!this.selectedYearStart) return;

      const yearStart = this.selectedYearStart;
      const yearEnd = this.selectedYearEnd || this.selectedYearStart;

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/total_births_range?start_year=${yearStart}&end_year=${yearEnd}`
        );
        const data = await response.json();
        this.birthData = data;
      } catch (error) {
        console.error(
          'Erreur lors de la récupération des naissances pour la plage :',
          error
        );
      }
    },
    formatNumber(number) {
      return number.toLocaleString('fr-FR');
    },
    calculateTotalBirths() {
      return this.birthData.reduce((total, data) => total + data.total_births, 0);
    },
  },
  mounted() {
    this.fetchTotalBirths();
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  margin-top: 15px;
}

.main-content {
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.35);
  margin-top: 15px;
}

.year-births-section {
  background: transparent;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: none !important;
  border: none !important;
}

.year-selector-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-top: 20px;
  background-color: transparent !important;
  box-shadow: none !important;
  border: none !important;
}

.year-selector-wrapper label {
  font-size: 1.2em;
  margin-bottom: 10px;
}

v-select {
  background-color: transparent !important;
  box-shadow: none !important;
  border: none !important;
}

.v-input__control {
  background-color: transparent !important;
  box-shadow: none !important;
  border: none !important;
}

.v-select__slot,
.v-select__selections {
  background-color: transparent !important;
  border: none !important;
}

.births-table-wrapper {
  margin-top: 20px;
}

.births-table {
  width: 100%;
  border-collapse: collapse;
}

.births-table th,
.births-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.births-table th {
  background-color: #6D2E46;
  color: white;
}

.births-table td {
  font-size: 1.2em;
}

.plot-section {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.35);
  max-width: 100%;
  overflow-x: auto;
}
</style>
