<template>
  <v-navigation-drawer app class="sidebar-container">
    <v-list>
      <v-list-item>
        <v-list-item-title class="filter-title">Filtres généraux</v-list-item-title>
      </v-list-item>
      <v-list-item>
        <v-text-field
          label="Prénom"
          v-model="filters.name"
          placeholder="Entrez un prénom"
        ></v-text-field>
      </v-list-item>
      <v-list-item>
        <v-text-field
          label="Sexe"
          v-model="filters.sexe"
          placeholder="Entrez un sexe"
        ></v-text-field>
      </v-list-item>
      <v-list-item>
        <v-select
          label="Date"
          v-model="filters.year"
          :items="years"
          placeholder="Sélectionnez une année"
        ></v-select>
      </v-list-item>
      <v-list-item>
        <v-btn @click="applyFilters">Appliquer les filtres</v-btn>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  data() {
    return {
      filters: {
        name: '',
        year: null,
      },
      years: Array.from({ length: 2021 - 1880 + 1 }, (v, k) => 1880 + k),
    };
  },
  methods: {
    applyFilters() {
      console.log('Filters applied:', this.filters);
    },
  },
};
</script>

<style scoped>
.v-navigation-drawer {
  background: #E1D7CD;
  padding: 10px;
}

.filter-title {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 10px;
}

.v-list-item {
  margin-bottom: 15px;
}

.v-btn {
  background-color: #1976D2;
  color: white;
}

.v-btn:hover {
  background-color: #135ba1;
}
</style>
