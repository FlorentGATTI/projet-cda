<template>
    <div class="sidebar-container">
      <v-navigation-drawer app>
        <v-list>
          <v-list-item
            v-for="(item, index) in items"
            :key="index"
            :to="item.route"
            class="sidebar-item"
            :class="{'sidebar-item-active': isActive(item.route)}"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
    </div>
  </template>
  
  <script>
  export default {
    name: 'SideBar',
    data() {
      return {
        items: [
          { title: 'Home', route: '/' },
          { title: 'Name Analysis', route: '/name-analysis' },
          { title: 'Global Statistics', route: '/global-stat' },
          { title: 'Stats Diversity', route: '/stats-diversity' },
          { title: 'Contact', route: '/contact' },
        ],
      }
    },
    methods: {
      isActive(route) {
        return this.$route.path === route;
      },
    },
  }
  </script>
  
  <style scoped>
  .v-list {
    padding: 0;
  }
  .v-navigation-drawer {
    background: linear-gradient(#cdc1b5, #E1D7CD);
    border-right: 0px solid #0B4678;
  }
  
  .v-list-item {
    transition: color 0.3s;
    background-color: transparent !important;
  }
  
  .v-list-item .v-list-item-title {
    color: #0B4678;
    font-weight: bold;
    font-size: 16px;
  }
  
  .v-list-item:hover .v-list-item-title,
  .v-list-item:focus .v-list-item-title {
    color: #6D2E46;
  }
  
  .sidebar-item-active .v-list-item-title {
    color: #A26769;
  }
  </style>
  