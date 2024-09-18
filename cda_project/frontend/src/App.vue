<template>
  <v-app @touchend="endTouch">
    <!-- Navbar -->
    <v-app-bar app color="primary" dark class="elevation-2 artistic-navbar sticky-navbar">
      <v-toolbar-title class="title">
        <img src="@/assets/logoCDA.png" alt="Logo" style="height: 50px;">
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Menu burger pour mobile -->
      <v-btn
        icon
        class="d-lg-none"
        @click="toggleNavbar"
        :color="navbarOpen ? 'secondary' : 'white'"
        aria-label="Toggle navigation"
        :aria-expanded="navbarOpen"
        aria-controls="nav-dropdown"
      >
        <v-icon>mdi-menu</v-icon>
      </v-btn>

      <!-- Desktop Navigation Links -->
      <v-row class="nav-buttons-desktop" align="center" justify="end" v-if="isDesktop">
        <v-btn v-for="link in navLinks" :key="link.path" class="nav-btn nav-btn-spacing" text @click="navigateTo(link.path)">
          {{ link.name }}
        </v-btn>
      </v-row>
    </v-app-bar>

    <!-- Menu déroulant pour le menu burger -->
    <transition name="fade">
      <v-row v-if="navbarOpen && !isDesktop" id="nav-dropdown" class="nav-dropdown" align="center" justify="center">
        <v-btn v-for="link in navLinks" :key="link.path" class="nav-btn-dropdown" text @click="navigateTo(link.path)">
          {{ link.name }}
        </v-btn>
      </v-row>
    </transition>

    <!-- Contenu principal avec sidebar -->
    <v-main :class="shouldShowSidebar ? 'with-sidebar' : 'without-sidebar'">
      <v-container fluid class="main-container">
        <!-- Sidebar (affichée uniquement pour certaines pages) -->
        <SideBar v-if="shouldShowSidebar" class="sidebar-desktop" @apply-filters="handleApplyFilters" :key="sidebarKey" ref="sidebarRef" />
        <!-- Page Content -->
        <v-container fluid class="content-container">
          <router-view :filters="filters" ref="statsDiversityRef" />
        </v-container>
      </v-container>
    </v-main>
  </v-app>
</template>


<script>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import SideBar from "./components/SideBar.vue";
import { debounce } from "lodash";

export default {
  name: "App",
  components: { SideBar },
  setup() {
    const router = useRouter();
    const route = useRoute();

    const navbarOpen = ref(false);
    const sidebarOpen = ref(false);
    const startX = ref(0);
    const statsDiversityRef = ref(null);
    const sidebarRef = ref(null);
    const sidebarKey = ref(0);

    const filters = ref({
      selectedRegionType: "state",
      region: null,
      year: null,
      sex: null,
      name: null,
    });

    const windowWidth = ref(window.innerWidth);
    const breakpoint = 1280;
    const isDesktop = computed(() => windowWidth.value >= breakpoint);

    const navLinks = [
      { name: "Accueil", path: "/" },
      { name: "Analyse des prénoms", path: "/name-analysis" },
      { name: "Statistiques globales", path: "/global-stat" },
      { name: "Diversité géographique", path: "/stats-diversity" },
      { name: "À propos", path: "/contact" },
    ];

    const shouldShowSidebar = computed(() => {
      return route.path === "/name-analysis" || route.path === "/stats-diversity";
    });

    const toggleNavbar = () => {
      navbarOpen.value = !navbarOpen.value;
    };

    const startTouch = (event) => {
      startX.value = event.touches[0].clientX;
    };

    const endTouch = (event) => {
      const endX = event.changedTouches[0].clientX;
      if (endX - startX.value > 100) {
        sidebarOpen.value = true;
      } else if (startX.value - endX > 100) {
        sidebarOpen.value = false;
      }
    };

    const navigateTo = (path) => {
      router.push(path);
      navbarOpen.value = false;
    };

    const handleResize = debounce(() => {
      windowWidth.value = window.innerWidth;
      if (isDesktop.value) {
        navbarOpen.value = false;
      }
    }, 100);

    const resetSidebarFilters = () => {
      sidebarKey.value += 1;
      if (sidebarRef.value) {
        sidebarRef.value.resetFilters();
      }
    };

    const handleApplyFilters = (appliedFilters) => {
      filters.value = { ...filters.value, ...appliedFilters };
      if (statsDiversityRef.value && statsDiversityRef.value.fetchAndDisplayData) {
        statsDiversityRef.value.fetchAndDisplayData();
      }
      resetSidebarFilters();
    };

    onMounted(() => {
      window.addEventListener("resize", handleResize);
      window.addEventListener("touchstart", startTouch, { passive: true });
    });

    onBeforeUnmount(() => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("touchstart", startTouch);
    });

    return {
      navbarOpen,
      sidebarOpen,
      isDesktop,
      route,
      navLinks,
      toggleNavbar,
      startTouch,
      endTouch,
      navigateTo,
      shouldShowSidebar,
      filters,
      statsDiversityRef,
      handleApplyFilters,
      sidebarRef,
      sidebarKey,
    };
  },
};
</script>

<style scoped>
/* Styles généraux */
body,
.v-application,
main {
  background-color: #f5f5f5; /* Couleur de fond légèrement plus claire */
  color: #2c3e50;
  font-family: "Arial", sans-serif;
  overflow-x: hidden;
}

/* Barre de navigation */
.v-app-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
  background-color: #A26769; /* Changement de la couleur de fond à #A26769 */
  padding: 10px 30px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.sticky-navbar {
  z-index: 100;
}

/* Sidebar desktop */
.sidebar-desktop {
  position: fixed;
  top: 64px;
  bottom: 0;
  left: 0;
  width: 250px;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1); /* Ombre plus douce */
  border-right: 1px solid #e0e0e0; /* Légère bordure pour séparer visuellement */
}

/* Sidebar mobile */
.mobile-sidebar {
  z-index: 90;
  background-color: #ffffff;
}

/* Conteneur principal */
.v-main {
  display: flex;
  flex-grow: 1;
  margin-top: 64px;
  padding: 30px; /* Plus d'espace pour aérer le contenu */
  box-sizing: border-box;
  overflow: auto;
}

.with-sidebar {
  margin-left: 250px;
}

.without-sidebar {
  margin-left: 0;
  padding: 30px 50px; /* Confort visuel accru pour les pages sans sidebar */
}

/* Conteneur de contenu */
.content-container {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #ffffff; /* Couleur de fond blanche pour un look épuré */
  border-radius: 8px; /* Coins arrondis pour un look moderne */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05); /* Légère ombre pour un effet flottant */
  padding: 20px;
}

/* Boutons de navigation */
.nav-btn {
  transition: transform 0.2s, background-color 0.2s, color 0.2s;
  color: #ffffff;
  font-weight: 600;
  padding: 10px 20px;
  background: linear-gradient(45deg, #A26769, #6d2e46); /* Dégradé avec les couleurs de la charte graphique */
}

.nav-btn:hover {
  transform: scale(1.1); /* Légère augmentation de taille au survol */
  background-color: #6d2e46; /* Couleur plus foncée de la charte pour le survol */
  color: #ffffff;
}

.nav-btn-spacing {
  margin-right: 15px; /* Plus d'espace entre les boutons */
}

.nav-btn-spacing:last-child {
  margin-right: 0;
}

/* Menu déroulant (burger menu) */
.nav-dropdown {
  position: absolute;
  top: 75px; /* Descend légèrement le menu déroulant pour éviter qu'il soit trop proche de la barre de navigation */
  width: 100%;
  background-color: #A26769; /* Couleur de fond du menu burger */
  z-index: 99;
  flex-direction: column;
  padding: 20px 0px; /* Augmentation du padding pour aérer davantage le menu */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2); /* Ombre douce pour un effet flottant */
}

.nav-btn-dropdown {
  color: #e1d7cd; /* Couleur de texte claire pour le contraste */
  font-weight: 600;
  padding: 15px 25px; /* Augmentation du padding pour agrandir les boutons */
  margin-bottom: 15px; /* Espace supplémentaire entre les boutons */
  border-bottom: 1px solid rgba(255, 255, 255, 0.2); /* Bordure subtile entre les éléments */
  width: 100%;
  text-align: center;
  background-color: transparent; /* Fond transparent pour un effet plus léger */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Transition pour les effets de hover */
}

.nav-btn-dropdown:hover {
  background-color: rgba(25, 118, 210, 0.8); /* Bleu plus clair de la charte au survol */
  transform: scale(1.05); /* Légère augmentation de la taille au survol */
}

.nav-btn-dropdown:last-child {
  margin-bottom: 0; /* Pas de marge après le dernier élément */
}

.nav-buttons-desktop .v-btn:last-child {
  margin-right: 25px; /* Ajustez cette valeur selon les besoins */
}


/* Boutons généraux */
.v-btn {
  background: linear-gradient(45deg, #1976d2, #0b4678); /* Dégradé utilisant les couleurs de la charte */
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.15); /* Ombre douce */
  color: #e1d7cd; /* Texte clair pour le contraste */
  font-weight: 600;
}

/* Effet de parallaxe */
.abstract-bg {
  background-attachment: fixed;
  background-size: cover;
}

/* Animations */
.slide-left-enter-active,
.slide-left-leave-active {
  transition: transform 0.3s ease;
}

.slide-left-enter,
.slide-left-leave-to {
  transform: translateX(-100%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* Responsivité */
@media (max-width: 1280px) {
  .v-main {
    margin-left: 0;
    padding: 20px;
  }

  .nav-buttons-desktop {
    display: none;
  }
}

@media (min-width: 1281px) {
  .nav-dropdown {
    display: none;
  }
}
</style>





