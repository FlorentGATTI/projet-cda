<template>
    <div id="app">
      <h1>Analyse des Prénoms des Bébés aux États-Unis</h1>
      <div class="year-selector">
        <label for="year">Sélectionnez une année :</label>
        <select id="year" v-model="selectedYear" @change="fetchData">
          <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
        </select>
      </div>
      <p class="total-births">Total des naissances en {{ selectedYear }} : {{ totalBirths }}</p>
      <PlotViewer v-model:year="selectedYear" />
    </div>
  </template>
  
  <script>
  import PlotViewer from '../components/PlotViewer.vue';
  
  export default {
    name: 'App',
    components: {
      PlotViewer
    },
    data() {
      return {
        years: Array.from({ length: 2021 - 1880 + 1 }, (v, k) => 1880 + k),
        selectedYear: 2001,
        totalBirths: 0,
      };
    },
    methods: {
      async fetchData() {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/total_births/${this.selectedYear}`);
          const data = await response.json();
          this.totalBirths = data.total_births;
          console.log(this.totalBirths);
        } catch (error) {
          console.error('Error fetching total births:', error);
        }
      },
    },
    mounted() {
      this.fetchData();
    },
  };
  </script>
  
  <style scoped>
  #app {
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
    font-family: 'Arial', sans-serif;
  }
  
  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
    color: #1976d2;
  }
  
  .year-selector {
    margin-bottom: 20px;
  }
  
  .total-births {
    font-size: 1.2em;
    margin-bottom: 20px;
  }
  </style>
  