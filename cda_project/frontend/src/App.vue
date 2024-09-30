<template>
  <v-app>
    <v-app-bar app color="primary" dark class="elevation-2 artistic-navbar sticky-navbar">
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
      <!--  <v-btn icon class="d-inline-flex d-lg-none" @click="toggleNavbar" :color="navbarOpen ? 'secondary' : 'white'" aria-label="Toggle navigation" :aria-expanded="navbarOpen" aria-controls="nav-dropdown">
        <v-icon>{{ navbarOpen ? "mdi-close" : "mdi-menu" }}</v-icon>  -->
      </v-btn>

      <v-row class="nav-buttons-desktop" align="center" justify="end" v-if="isDesktop">
        <v-btn v-for="link in navLinks" :key="link.path" class="nav-btn nav-btn-spacing" text @click="navigateTo(link.path)" :class="{ 'active-link': isActiveRoute(link.path) }">
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
    <!-- <div class="navbar-dropdown" :class="{ 'navbar-open': navbarOpen }">
      <v-list>
        <v-list-item v-for="link in navLinks" :key="link.path" @click="navigateTo(link.path)" :class="{ 'active-link': isActiveRoute(link.path) }">
          <v-list-item-title>{{ link.name }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </div>

    <div @touchstart="startTouch" @touchmove="moveTouch" @touchend="endTouch">
      <v-main :class="{ 'with-sidebar': shouldShowSidebar && sidebarOpen, 'without-sidebar': !shouldShowSidebar || !sidebarOpen }">
        <v-container fluid class="main-container">
          <SideBar v-if="shouldShowSidebar" :class="['sidebar-desktop', { 'sidebar-open': sidebarOpen }]" @apply-filters="handleApplyFilters" :key="sidebarKey" ref="sidebarRef" />
          <v-container fluid class="content-container">
            <router-view :filters="filters" ref="statsDiversityRef" />
          </v-container> -->
        </v-container>
      </v-main>
    </div>
  </v-app>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useDisplay } from "vuetify";
import SideBar from "./components/SideBar.vue";
import debounce from "lodash/debounce";
import { useSwipe } from "./composables/useSwipe";
import { nextTick } from 'vue'


export default {
  name: "App",
  components: { SideBar },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const { lgAndUp } = useDisplay();

    const navbarOpen = ref(false);
    const sidebarOpen = ref(false);
    const statsDiversityRef = ref(null);
    const sidebarRef = ref(null);
    const sidebarKey = ref(0);

    const filters = ref({
      selectedType: "state",
      selectedValue: null,
      year: null,
      sex: null,
      name: null,
    });

    const isDesktop = computed(() => lgAndUp.value);

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
      sidebarOpen.value = false;
      navbarOpen.value = !navbarOpen.value;
    };

    const { startTouch, moveTouch, endTouch } = useSwipe({
      onSwipeRight: () => {
        if (shouldShowSidebar.value && !sidebarOpen.value) {
          sidebarOpen.value = true;
        }
      },
      onSwipeLeft: () => {
        if (shouldShowSidebar.value && sidebarOpen.value) {
          sidebarOpen.value = false;
        }
      },
    });

    const navigateTo = (path) => {
      router.push(path);
      navbarOpen.value = false;
      if (path !== "/stats-diversity") {
        sidebarOpen.value = false;
      }
    };

    const isActiveRoute = (path) => {
      return route.path === path;
    };

    const handleResize = debounce(() => {
      if (isDesktop.value) {
        navbarOpen.value = false;
        sidebarOpen.value = false;
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
        nextTick(() => {
          statsDiversityRef.value.fetchAndDisplayData();
        });
      }
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

    watch(route, () => {
      if (shouldShowSidebar.value) {
        resetSidebarFilters();
      } else {
        sidebarOpen.value = false;
      }
    });

    return {
      navbarOpen,
      sidebarOpen,
      isDesktop,
      route,
      navLinks,
      toggleNavbar,
      startTouch,
      moveTouch,
      endTouch,
      navigateTo,
      isActiveRoute,
      shouldShowSidebar,
      filters,
      updateFilters,
      loggedIn,
      logout,
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
  background-color: #f5f5f5;
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
  background-color: #a26769;
  padding: 10px 30px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
}

.sticky-navbar {
  z-index: 1000;
}

/* Navbar dropdown */
.navbar-dropdown {
  position: fixed;
  top: 74px;
  left: 0;
  width: 100%;
  height: 35%;
  background-color: rgba(162, 103, 105, 0.95);
  z-index: 999;
  transform: translateY(-100%);
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  visibility: hidden;
  opacity: 0;
  transition: transform 0.3s ease-in-out, opacity 0.3s ease-in-out, visibility 0.3s ease-in-out;
  pointer-events: none;
}

.navbar-open {
  transform: translateY(0);
  visibility: visible;
  opacity: 1;
  pointer-events: auto;
}

.navbar-dropdown .v-list {
  padding: 16px 0;
  background-color: transparent;
}

.navbar-dropdown .v-list-item {
  width: 100%;
  top: 10px;
  height: 40%;
  padding: 0 24px;
  margin-bottom: 8px;
  color: #ffffff;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.navbar-dropdown .v-list-item:hover,
.navbar-dropdown .v-list-item.active-link {
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.05);
}

.navbar-dropdown .v-list-item-title {
  text-align: center;
  color: #ffffff;
  font-size: 18px;
}

/* Sidebar */
.sidebar-desktop {
  position: fixed;
  top: 64px;
  bottom: 0;
  left: -250px;
  width: 250px;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  border-right: 1px solid #e0e0e0;
  transition: transform 0.3s ease-in-out;
  z-index: 98;
}

.sidebar-open {
  transform: translateX(250px);
}

/* Conteneur principal */
.v-main {
  display: flex;
  flex-grow: 1;
  margin-top: 64px;
  padding: 30px;
  box-sizing: border-box;
  overflow: auto;
  transition: margin-left 0.3s ease-in-out;
}

.with-sidebar {
  margin-left: 250px;
}

.without-sidebar {
  margin-left: 0;
  padding: 30px 50px;
}

/* Conteneur de contenu */
.content-container {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

/* Boutons de navigation */
.nav-btn {
  transition: transform 0.2s, background-color 0.2s, color 0.2s;
  color: #ffffff;
  font-weight: 600;
  padding: 10px 20px;
  background: linear-gradient(45deg, #a26769, #6d2e46);
}

.nav-btn:hover,
.nav-btn.active-link {
  transform: scale(1.05);
  background-color: #6d2e46;
  color: #ffffff;
}

.nav-btn-spacing {
  margin-right: 15px;
}

.nav-btn-spacing:last-child {
  margin-right: 0;
}

/* Menu déroulant (burger menu) */
.navbar-dropdown .v-list {
  padding: 0;
  background-color: transparent;
}

.navbar-dropdown .v-list-item {
  min-height: 48px;
  color: #ffffff;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.navbar-dropdown .v-list-item:hover,
.navbar-dropdown .v-list-item.active-link {
  background-color: rgba(25, 118, 210, 0.8);
  transform: scale(1.05);
}

.navbar-dropdown .v-list-item-title {
  text-align: center;
  color: #ffffff;
}

.nav-buttons-desktop .v-btn:last-child {
  margin-right: 25px;
}

/* Boutons généraux */
.v-btn {
  background: linear-gradient(45deg, #1976d2, #0b4678);
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.15);
  color: #e1d7cd;
  font-weight: 600;
}

/* Effet de parallaxe */
.abstract-bg {
  background-attachment: fixed;
  background-size: cover;
}

/* Responsivité */
@media (max-width: 1420px) {
  .v-main {
    margin-left: 0;
    padding: 20px;
  }

  .nav-buttons-desktop {
    display: none;
  }

  .sidebar-desktop {
    transform: translateX(-250px);
  }

  .with-sidebar .sidebar-desktop {
    transform: translateX(0);
  }
}

@media (min-width: 1421px) {
  .navbar-dropdown {
    display: none;
  }
}
</style>
