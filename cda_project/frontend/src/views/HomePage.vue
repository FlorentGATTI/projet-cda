<template>
  <v-container fluid class="home-container">
    <!-- En-tête de la page -->
    <v-row class="text-center">
      <v-col>
        <h1 class="main-title">Analyse des Prénoms aux États-Unis</h1>
        <p class="subtitle">
          Découvrez les tendances des prénoms aux États-Unis au fil des années.
        </p>
      </v-col>
    </v-row>

    <!-- Section d'introduction -->
    <v-row class="introduction-section">
      <v-col cols="12" md="8" class="mx-auto">
        <h2>Introduction</h2>
        <p>
          Ce projet vous permet d'explorer les données sur les prénoms donnés aux
          bébés aux États-Unis. Grâce à des graphiques interactifs, vous pouvez
          visualiser les tendances des prénoms, comparer la popularité de différents
          prénoms au fil des années, et bien plus encore.
        </p>
      </v-col>
    </v-row>

    <!-- Section de navigation -->
    <v-row class="navigation-section text-center">
      <v-col cols="12" md="4" class="mx-auto">
        <v-btn
          class="nav-button"
          large
          color="primary"
          @click="navigateTo('/name-analysis')"
        >
          Analyse des Prénoms
        </v-btn>
      </v-col>
      <v-col cols="12" md="4" class="mx-auto">
        <v-btn
          class="nav-button"
          large
          color="primary"
          @click="navigateTo('/global-stat')"
        >
          Statistiques Globales
        </v-btn>
      </v-col>
      <v-col cols="12" md="4" class="mx-auto">
        <v-btn
          class="nav-button"
          large
          color="primary"
          @click="navigateTo('/stats-diversity')"
        >
          Diversité Géographique
        </v-btn>
      </v-col>
    </v-row>

    <!-- Section d'informations supplémentaires -->
    <v-row class="extra-info-section">
      <v-col cols="12" md="8" class="mx-auto">
        <h2>Pourquoi ce projet ?</h2>
        <p>
          L'étude des prénoms permet d'avoir une perspective unique sur les tendances
          culturelles, sociales et démographiques. Les prénoms sont plus qu'une simple
          étiquette, ils reflètent des époques, des influences, et même des changements
          de la société.
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "HomePage",
  setup() {
    const router = useRouter();

    const navigateTo = (path) => {
      router.push(path);
    };

    return {
      navigateTo,
    };
  },
};
</script>

<style scoped>
.home-container {
  background-color: #f5f5f5;
  padding: 40px;
  font-family: 'Roboto', sans-serif;
}

.main-title {
  font-size: 3em;
  color: #1976D2;
  margin-bottom: 20px;
}

.subtitle {
  font-size: 1.5em;
  color: #6D2E46;
  margin-bottom: 40px;
}

.introduction-section {
  margin-bottom: 60px;
}

.navigation-section {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 60px;
}

.nav-button {
  width: 100%;
  margin-bottom: 20px;
}

.extra-info-section h2 {
  color: #1976D2;
  margin-bottom: 20px;
}

.extra-info-section p {
  font-size: 1.2em;
  color: #2c3e50;
}
</style>
