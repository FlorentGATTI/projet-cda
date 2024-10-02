<template>
  <v-app>
    <v-app-bar v-if="showNavbar" app class="navbar">
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
        <v-btn v-for="link in navLinks" :key="link.path" class="nav-btn nav-btn-spacing" text @click="navigateTo(link.path)">
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
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
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

    const windowWidth = ref(window.innerWidth);
    const breakpoint = 1280;
    const isDesktop = computed(() => windowWidth.value >= breakpoint);

    const navLinks = [
      { name: "Accueil", path: "/" },
      { name: "Analyse des prénoms", path: "/name-analysis" },
      { name: "Statistiques globales", path: "/global-stat" },
      { name: "Diversité géographique", path: "/stats-diversity" },
      // { name: "À propos", path: "/contact" },
    ];

    const shouldShowSidebar = computed(() => {
      return route.path === "/stats-diversity";
    });

    const showNavbar = computed(() => {
      return route.path !== "/login";
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
      endTouch,
      navigateTo,
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
  background-color: #1e1e2f;
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

/* Barre de navigation */
.v-app-bar {
  background-color: #1976d2 !important;
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
  background-color: rgba(25, 118, 210, 0.95);
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

/* Sidebar desktop */
.sidebar-desktop {
  position: fixed;
  top: 64px;
  bottom: 0;
  left: 0;
  width: 250px;
  background-color: #ffffff;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  border-right: 1px solid #e0e0e0;
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
  padding: 30px;
  box-sizing: border-box;
  overflow: auto;
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
  background-color: #27293d;
  border-radius: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
  padding: 20px;
}

/* Boutons de navigation */
.nav-btn {
  transition: transform 0.2s, background-color 0.2s, color 0.2s;
  color: #ffffff !important;
  font-weight: 600;
  padding: 5px 15px;
  background: linear-gradient(45deg, #1976d2, #1565c0);
  min-width: 0;
}

.nav-btn:hover,
.nav-btn.active-link {
  transform: scale(1.05);
  background-color: #1565c0;
}

.nav-btn-spacing {
  margin-right: 10px;
}

.nav-buttons-desktop .v-btn:last-child {
  margin-right: 25px;
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

  .sidebar-desktop {
    transform: translateX(-250px);
  }

  .with-sidebar .sidebar-desktop {
    transform: translateX(0);
  }

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