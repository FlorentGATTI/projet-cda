<template>
  <v-app @touchstart="startTouch" @touchend="endTouch">
    <!-- Navbar -->
    <v-app-bar class="navbar">
      <v-toolbar-title class="title">
        <img src="@/assets/logoCDA.png" alt="Logo" style="height: 50px" />
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Bouton de déconnexion pour desktop -->
      <v-btn v-if="loggedIn" class="nav-btn" text @click="logout">
        Déconnexion
      </v-btn>

      <!-- Menu burger pour mobile -->
      <v-btn icon class="d-lg-none" @click="toggleNavbar" :color="navbarOpen ? 'secondary' : 'white'" aria-label="Toggle navigation" :aria-expanded="navbarOpen" aria-controls="nav-dropdown">
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
        <!-- Bouton de déconnexion pour mobile -->
        <v-btn v-if="loggedIn" class="nav-btn-dropdown" text @click="logout">
          Déconnexion
        </v-btn>
      </v-row>
    </transition>

    <!-- Contenu principal avec sidebar -->
    <v-main :class="shouldShowSidebar ? 'with-sidebar' : 'without-sidebar'">
      <v-container fluid class="main-container">
        <!-- Sidebar (affichée uniquement pour certaines pages) -->
        <SideBar v-if="shouldShowSidebar" class="sidebar-desktop" @filters-applied="updateFilters" />

        <!-- Page Content -->
        <v-container fluid class="content-container">
          <router-view :filters="filters" />
        </v-container>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import SideBar from "./components/SideBar.vue";
import { debounce } from "lodash"; // Import lodash debounce function

export default {
  name: "App",
  components: { SideBar },
  setup() {
    const router = useRouter();
    const route = useRoute();

    const navbarOpen = ref(false);
    const sidebarOpen = ref(false);
    const startX = ref(0);

    const filters = ref({ name: "", sexe: "", year: null });

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
      return route.path === "/stats-diversity";
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

    const updateFilters = (newFilters) => {
      filters.value = newFilters;
    };

    const loggedIn = computed(() => !!localStorage.getItem("user")); // Vérifie si l'utilisateur est connecté

    const logout = () => {
      localStorage.removeItem("user"); // Suppression de l'utilisateur du localStorage
      router.push("/login"); // Redirection vers la page de connexion
    };

    onMounted(() => {
      window.addEventListener("resize", handleResize);
    });

    onBeforeUnmount(() => {
      window.removeEventListener("resize", handleResize);
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
      updateFilters,
      loggedIn,
      logout,
    };
  },
};
</script>

<style scoped>
/* Styles généraux */
body,
.v-application,
main {
  background-color: #1e1e2f; /* Couleur de fond légèrement plus claire */
  color: #9a9a9a;
  font-family: "Arial", sans-serif;
  overflow-x: hidden;
}

.main-title {
    color: #9a9a9a;
    font-size: 3em;
  }

.v-toolbar {
  background-color: #1e1e2f !important;
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
  background-color: #27293d; /* Couleur de fond blanche pour un look épuré */
  border-radius: 8px; /* Coins arrondis pour un look moderne */
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05); /* Légère ombre pour un effet flottant */
  padding: 20px;
}

/* Boutons de navigation */
.nav-btn {
  transition: transform 0.2s, background-color 0.2s, color 0.2s;
  color: #ffffff;
}

.nav-btn:hover {
  transform: scale(1.1); /* Légère augmentation de taille au survol */
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
  top: 70px;
  right: 0;
  width: 100%;
  z-index: 99;
  flex-direction: column;
  padding-top: 20px;
  backdrop-filter: blur(40px);
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
}

.nav-btn-dropdown {
  margin-bottom: 15px; /* Espace supplémentaire entre les boutons */
  width: 500px;
  text-align: center;
  background-color: transparent; /* Fond transparent pour un effet plus léger */
  transition: background-color 0.3s ease, transform 0.3s ease; /* Transition pour les effets de hover */
}

.nav-btn-dropdown:hover {
  transform: scale(1.05); /* Légère augmentation de la taille au survol */
}

.nav-buttons-desktop .v-btn:last-child {
  margin-right: 25px; /* Ajustez cette valeur selon les besoins */
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