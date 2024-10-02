<template>
  <v-container fluid class="home-container">
    <!-- En-tête de la page -->
    <v-row class="text-center">
      <v-col>
        <h1 class="main-title">Analyse des Prénoms aux États-Unis</h1>
        <p class="subtitle">Découvrez les tendances des prénoms aux États-Unis au fil des années.</p>
      </v-col>
    </v-row>

    <!-- Section d'introduction -->
    <v-row class="introduction-section">
      <v-col cols="12" md="8" class="mx-auto">
        <h2>Introduction</h2>
        <p>Ce projet vous permet d'explorer les données sur les prénoms donnés aux bébés aux États-Unis. Grâce à des graphiques interactifs, vous pouvez visualiser les tendances des prénoms, comparer la popularité de différents prénoms au fil des années, et bien plus encore.</p>
      </v-col>
    </v-row>

    <!-- Section de l'objectif du projet -->
    <v-row class="objective-section">
      <v-col cols="12" md="8" class="mx-auto">
        <h2>Objectif du Projet</h2>
        <p>Ce projet vise à analyser les données fournies par l'administration américaine de la sécurité sociale pour identifier des tendances culturelles et sociales dans l'attribution des prénoms.</p>
      </v-col>
    </v-row>

    <!-- Section des fonctionnalités clés -->
    <v-row class="features-section">
      <v-col cols="12" class="text-center">
        <h2 style="color: #1976d2">Fonctionnalités Clés</h2>
      </v-col>
      <v-col cols="12" md="4" class="feature-item">
        <v-icon large class="feature-icon" color="#004ba0">mdi-chart-bar</v-icon>
        <!-- Vérifie le préfixe -->
        <h3 style="color: #ffffff">Analyse de la Diversité des Prénoms</h3>
        <p style="color: #e0e0e0">Comparez la diversité des prénoms à travers les années.</p>
      </v-col>
      <v-col cols="12" md="4" class="feature-item">
        <v-icon large class="feature-icon" color="#004ba0">mdi-ruler</v-icon>
        <h3 style="color: #ffffff">Analyse par Longueur de Prénom</h3>
        <p style="color: #e0e0e0">Découvrez les tendances liées à la longueur des prénoms.</p>
      </v-col>
      <v-col cols="12" md="4" class="feature-item">
        <v-icon large class="feature-icon" color="#004ba0">mdi-map</v-icon>
        <h3 style="color: #ffffff">Analyse Géographique</h3>
        <p style="color: #e0e0e0">Explorez les différences de popularité des prénoms par état et par territoires.</p>
      </v-col>
    </v-row>

    <!-- Section d'informations supplémentaires -->
    <v-row class="extra-info-section">
      <v-col cols="12" md="8" class="mx-auto">
        <h2>Pourquoi ce projet ?</h2>
        <p>L'étude des prénoms permet d'avoir une perspective unique sur les tendances culturelles, sociales et démographiques. Les prénoms sont plus qu'une simple étiquette, ils reflètent des époques, des influences, et même des changements de la société.</p>
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
  padding: 20px;
}

.subtitle {
  font-size: 1.5em;
  color: #E0E0E0; 
  margin-bottom: 20px;
}

.introduction-section {
  margin-bottom: 10px;
}

.introduction-section, .objective-section, .extra-info-section {
  color: #E0E0E0; 
}

h2 {
  color: #1976D2; 
}

.feature-icon {
  color: #004ba0; 
}

.objective-section {
  margin-top: 20px;
}

.features-section {
  margin: 40px 0;
}

.feature-item {
  text-align: center;
  padding: 20px;
}

h3 {
  margin: 10px 0;
  color: #FFFFFF;
}
</style>
