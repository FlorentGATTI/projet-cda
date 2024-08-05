<template>
  <div id="app">
    <h1>Top Names in 2001</h1>
    <p>{{ names.total_births }}</p>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      names: [],
    };
  },
  methods: {
    async fetchNames() {
      try {
        const response = await fetch('http://127.0.0.1:8000/total_births/2001');
        const data = await response.json();
        this.names = data;
        console.log(this.names);
      } catch (error) {
        console.error('Error fetching names:', error);
      }
    },
  },
  mounted() {
    this.fetchNames();
  },
};
</script>

<style scoped>
#app {
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
ul {
  text-decoration: none;
}
</style>
