<template>
  <v-app>
    <v-app-bar v-if="showNavbar" app color="primary" dark class="elevation-2 artistic-navbar sticky-navbar">
      <v-toolbar-title class="title">
        <img src="@/assets/logoCDA.png" alt="Logo" style="height: 50px" />
      </v-toolbar-title>

      <v-spacer></v-spacer>

      <!-- Menu burger pour mobile -->
      <v-btn icon class="d-lg-none" @click="toggleNavbar" :color="navbarOpen ? 'secondary' : 'white'" aria-label="Toggle navigation" :aria-expanded="navbarOpen" aria-controls="nav-dropdown">
        <v-icon>{{ navbarOpen ? "mdi-close" : "mdi-menu" }}</v-icon>
      </v-btn>

      <!-- Boutons de navigation pour desktop -->
      <v-row class="nav-buttons-desktop" align="center" justify="end" v-if="isDesktop">
        <v-btn v-for="link in navLinks" :key="link.path" class="nav-btn nav-btn-spacing" text @click="navigateTo(link.path)" :class="{ 'active-link': isActiveRoute(link.path) }">
          {{ link.name }}
        </v-btn>
        <v-btn v-if="loggedIn" class="nav-btn" text @click="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </v-row>
    </v-app-bar>

    <!-- Menu déroulant central pour le menu burger -->
    <v-expand-transition>
      <div v-if="showNavbar && navbarOpen && !isDesktop" class="nav-dropdown">
        <v-container class="d-flex flex-column align-center justify-center h-100">
          <v-btn v-for="link in navLinks" :key="link.path" class="nav-btn-dropdown mb-2" text @click="navigateTo(link.path)">
            {{ link.name }}
          </v-btn>
          <v-btn v-if="loggedIn" class="nav-btn-dropdown" text @click="logout">
            <v-icon left>mdi-logout</v-icon>
            Déconnexion
          </v-btn>
        </v-container>
      </div>
    </v-expand-transition>

    <!-- Contenu principal avec sidebar -->
    <div @touchstart="startTouch" @touchmove="moveTouch" @touchend="endTouch">
      <v-main :class="{ 'with-sidebar': shouldShowSidebar && sidebarOpen, 'without-sidebar': !shouldShowSidebar || !sidebarOpen }">
        <v-container fluid class="main-container">
          <SideBar v-if="shouldShowSidebar" :class="['sidebar-desktop', { 'sidebar-open': sidebarOpen }]" @apply-filters="handleApplyFilters" :key="sidebarKey" ref="sidebarRef" />
          <v-container fluid class="content-container">
            <router-view :filters="filters" ref="statsDiversityRef" />
          </v-container>
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
import { nextTick } from "vue";

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
    const isLoggedIn = ref(false);

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

    const showNavbar = computed(() => {
      return route.path !== "/login";
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

    const logout = () => {
      localStorage.removeItem("user");
      isLoggedIn.value = false;
      router.push("/login");
    };

    const checkLoginStatus = () => {
      isLoggedIn.value = !!localStorage.getItem("user");
    };

    onMounted(() => {
      window.addEventListener("resize", handleResize);
      checkLoginStatus();
      window.addEventListener("storage", checkLoginStatus);
    });

    onBeforeUnmount(() => {
      window.removeEventListener("resize", handleResize);
      window.removeEventListener("storage", checkLoginStatus);
    });

    watch(route, () => {
      if (shouldShowSidebar.value) {
        resetSidebarFilters();
      } else {
        sidebarOpen.value = false;
      }
      checkLoginStatus();
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
      loggedIn: isLoggedIn,
      logout,
      statsDiversityRef,
      handleApplyFilters,
      sidebarRef,
      sidebarKey,
      showNavbar,
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
  background-color: #1976d2 !important; /* Retour au bleu */
  padding: 0 30px;
}

.sticky-navbar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1000;
}

/* Menu déroulant */
.nav-dropdown {
  position: fixed;
  top: 64px;
  left: 0;
  width: 100%;
  height: calc(100vh - 64px);
  background-color: rgba(25, 118, 210, 0.95); /* Bleu avec transparence */
  z-index: 999;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.nav-btn-dropdown {
  width: 80%;
  max-width: 300px;
  margin-bottom: 10px;
  color: #ffffff !important;
  font-size: 1.2rem;
  text-transform: none;
  letter-spacing: normal;
}

.nav-btn-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.2);
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

/* Boutons de navigation */
.nav-btn {
  color: #ffffff !important;
  font-weight: 600;
  padding: 5px 15px;
  background: linear-gradient(45deg, #1976d2, #1565c0); /* Dégradé de bleu */
  min-width: 0;
  transition: transform 0.2s, background-color 0.2s;
  right: 15px;
}

.nav-btn:hover,
.nav-btn.active-link {
  transform: scale(1.05);
  background-color: #1565c0;
}

.nav-btn-spacing {
  margin-right: 10px;
}

/* Responsivité */
@media (max-width: 1420px) {
  .v-main {
    margin-left: 0;
    padding: 20px;
  }

  .sidebar-desktop {
    transform: translateX(-250px);
  }

  .with-sidebar .sidebar-desktop {
    transform: translateX(0);
  }
}

@media (max-width: 1280px) {
  .nav-buttons-desktop {
    display: none;
  }
}

@media (min-width: 1281px) and (max-width: 1420px) {
  .nav-buttons-desktop {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
  }

  .nav-btn {
    font-size: 0.9rem;
    padding: 4px 8px;
    margin-bottom: 4px;
  }
}

@media (min-width: 1421px) {
  .nav-dropdown {
    display: none;
  }
}
</style>
