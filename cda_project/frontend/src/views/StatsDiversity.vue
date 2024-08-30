<template>
  <v-container fluid>
    <h2>Diversité Géographique</h2>
    <div id="map" class="map-container"></div>
  </v-container>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";

export default {
  name: "StatsDiversity",
  props: {
    filters: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      map: null,
      usaBounds: [
        [24.396308, -125.0], // Sud-ouest
        [49.384358, -66.93457], // Nord-est
      ],
    };
  },
  watch: {
    filters: {
      handler() {
        this.applyFilters();
      },
      deep: true,
    },
  },
  mounted() {
    console.log("Montage de la carte");
    this.map = L.map("map", {
      maxBounds: this.usaBounds, // Appliquer les limites de la carte
      maxBoundsViscosity: 1.0, // Rendre les limites plus strictes
      minZoom: 4,
      maxZoom: 10, // Limite de zoom
    }).setView([39.8283, -98.5795], 4);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: "© OpenStreetMap contributors",
    }).addTo(this.map);

    this.applyFilters(); // Charger les données initiales
  },
  methods: {
    async applyFilters() {
      console.log("Application des filtres avec :", this.filters);

      // Vider la carte avant d'ajouter les nouvelles données
      this.map.eachLayer((layer) => {
        if (layer instanceof L.CircleMarker) {
          this.map.removeLayer(layer);
          console.log("Marqueur retiré :", layer);
        }
      });

      await this.loadStateData();
      await this.loadTerritoryData();
    },
    async loadStateData() {
      try {
        console.log("Chargement des données des États avec filtres :", this.filters);
        const queryParams = new URLSearchParams(this.filters);
        const response = await fetch(`/api/names_by_state?${queryParams}`);
        console.log("Réponse de l'API des États :", response);

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const stateData = await response.json();
        console.log("Données des États reçues :", stateData);

        if (!Array.isArray(stateData) || stateData.length === 0) {
          console.error("Pas de données trouvées pour les États");
          return;
        }

        stateData.forEach((record) => {
          const coordinates = this.getCoordinatesForState(record.State);
          if (coordinates) {
            console.log(`Ajout du marqueur pour ${record.Name} à ${coordinates}`);
            const marker = L.circleMarker(coordinates, {
              radius: 8,
              fillColor: "#1976D2",
              color: "#1976D2",
              weight: 1,
              opacity: 1,
              fillOpacity: 0.8,
            }).addTo(this.map);

            marker.bindPopup(`<strong>${record.Name}</strong><br>${record.Count} occurrences in ${record.Year}<br>State: ${record.State}`);
          } else {
            console.warn(`Pas de coordonnées trouvées pour l'état: ${record.State}`);
          }
        });
      } catch (error) {
        console.error("Erreur lors du chargement des données des États :", error);
      }
    },
    async loadTerritoryData() {
      try {
        console.log("Chargement des données des Territoires avec filtres :", this.filters);
        const queryParams = new URLSearchParams(this.filters);
        const response = await fetch(`/api/names_by_territory?${queryParams}`);
        console.log("Réponse de l'API des Territoires :", response);

        if (!response.ok) {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }

        const territoryData = await response.json();
        console.log("Données des Territoires reçues :", territoryData);

        territoryData.forEach((record) => {
          const coordinates = this.getCoordinatesForState(record.Territory);
          if (coordinates) {
            console.log(`Ajout du marqueur pour ${record.Name} à ${coordinates}`);
            const marker = L.circleMarker(coordinates, {
              radius: 8,
              fillColor: "#1976D2",
              color: "#1976D2",
              weight: 1,
              opacity: 1,
              fillOpacity: 0.8,
            }).addTo(this.map);

            marker.bindPopup(`<strong>${record.Name}</strong><br>${record.Count} occurrences in ${record.Year}<br>Territory: ${record.Territory}`);
          } else {
            console.warn(`Pas de coordonnées trouvées pour le territoire: ${record.Territory}`);
          }
        });

        const bounds = L.latLngBounds(territoryData.map((record) => this.getCoordinatesForState(record.Territory)).filter(Boolean));

        if (bounds.isValid()) {
          console.log("Ajustement des limites de la carte");
          this.map.fitBounds(bounds);
        } else {
          console.error("Impossible d'ajuster les limites de la carte : Les limites ne sont pas valides.");
        }
      } catch (error) {
        console.error("Erreur lors du chargement des données des Territoires :", error);
      }
    },
    getCoordinatesForState(stateOrTerritory) {
      const coordinates = {
        AL: [-86.9023, 32.3182], // Alabama
        AK: [-154.493062, 63.588753], // Alaska
        AZ: [-111.093731, 34.048928], // Arizona
        AR: [-92.199997, 34.746481], // Arkansas
        CA: [-119.417931, 36.778259], // California
        CO: [-105.782067, 39.550051], // Colorado
        CT: [-72.755371, 41.603221], // Connecticut
        DE: [-75.52767, 38.910832], // Delaware
        FL: [-81.515754, 27.664827], // Florida
        GA: [-82.900075, 32.165622], // Georgia
        HI: [-155.582782, 19.896766], // Hawaii
        ID: [-114.742041, 44.068202], // Idaho
        IL: [-89.398528, 40.633125], // Illinois
        IN: [-86.134902, 40.267194], // Indiana
        IA: [-93.097702, 41.878003], // Iowa
        KS: [-98.484246, 39.011902], // Kansas
        KY: [-84.270018, 37.839333], // Kentucky
        LA: [-92.145024, 30.984298], // Louisiana
        ME: [-69.445469, 45.253783], // Maine
        MD: [-76.641271, 39.045755], // Maryland
        MA: [-71.382437, 42.407211], // Massachusetts
        MI: [-85.602364, 44.314844], // Michigan
        MN: [-94.6859, 46.729553], // Minnesota
        MS: [-89.398528, 32.354668], // Mississippi
        MO: [-91.831833, 37.964253], // Missouri
        MT: [-110.362566, 46.879682], // Montana
        NE: [-99.901813, 41.492537], // Nebraska
        NV: [-116.419389, 38.80261], // Nevada
        NH: [-71.572395, 43.193852], // New Hampshire
        NJ: [-74.405661, 40.058324], // New Jersey
        NM: [-105.032363, 34.97273], // New Mexico
        NY: [-74.005973, 40.712776], // New York
        NC: [-79.0193, 35.759573], // North Carolina
        ND: [-101.002012, 47.551493], // North Dakota
        OH: [-82.907123, 40.417287], // Ohio
        OK: [-97.516428, 35.007752], // Oklahoma
        OR: [-120.554201, 43.804133], // Oregon
        PA: [-77.194525, 41.203322], // Pennsylvania
        RI: [-71.477429, 41.580095], // Rhode Island
        SC: [-81.163725, 33.836081], // South Carolina
        SD: [-99.901813, 43.969515], // South Dakota
        TN: [-86.580447, 35.517491], // Tennessee
        TX: [-99.901813, 31.968599], // Texas
        UT: [-111.093731, 39.32098], // Utah
        VT: [-72.577841, 44.558803], // Vermont
        VA: [-78.656894, 37.431573], // Virginia
        WA: [-120.740138, 47.751074], // Washington
        WV: [-80.454903, 38.597626], // West Virginia
        WI: [-89.398528, 43.78444], // Wisconsin
        WY: [-107.290284, 43.075968], // Wyoming
        DC: [-77.036871, 38.907192], // Washington D.C.
        AS: [-170.132217, -14.271], // American Samoa
        GU: [144.793731, 13.444304], // Guam
        MP: [145.750967, 15.0979], // Northern Mariana Islands
        PR: [-66.590149, 18.220833], // Puerto Rico
        VI: [-64.896335, 18.335765], // U.S. Virgin Islands
        UM: [166.614013, 19.282319], // U.S. Minor Outlying Islands
        PI: [125.9668, 8.4606], // Philippines (ancienne région sous US)
      };

      console.log(`Coordonnées pour ${stateOrTerritory} :`, coordinates[stateOrTerritory]);
      return coordinates[stateOrTerritory] || null;
    },
  },
};
</script>

<style scoped>
.map-container {
  height: 100%;
  width: 100%;
  position: absolute;
  top: 0;
  bottom: 0;
  right: 0;
  left: 0;
}
</style>
