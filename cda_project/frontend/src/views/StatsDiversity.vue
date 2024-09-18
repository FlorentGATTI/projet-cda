<template>
  <div class="stats-diversity-container">
    <div ref="mapContainer" class="map-container"></div>
    <div v-if="!filtersApplied" class="map-overlay">
      <p>Veuillez appliquer les filtres pour afficher les données sur la carte.</p>
    </div>
    <div v-if="noDataFound" class="map-overlay">
      <p>Aucune donnée trouvée pour les filtres sélectionnés.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, nextTick } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { getFullStateName, getFullTerritoryName, getStateCoordinates, getTerritoryCoordinates } from "../../../data/stateTerritoryMappings";

export default {
  name: "StatsDiversity",
  props: {
    filters: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const mapContainer = ref(null);
    const map = ref(null);
    const filtersApplied = ref(false);
    const noDataFound = ref(false);

    const initializeMap = () => {
      if (map.value || !mapContainer.value) return;

      map.value = L.map(mapContainer.value, {
        center: [37.8, -96],
        zoom: 4,
        zoomControl: false,
        dragging: false,
        touchZoom: false,
        doubleClickZoom: false,
        scrollWheelZoom: false,
        boxZoom: false,
        keyboard: false,
      });

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map.value);
    };

    const clearMapLayers = () => {
      if (!map.value) return;
      map.value.eachLayer((layer) => {
        if (!(layer instanceof L.TileLayer)) {
          map.value.removeLayer(layer);
        }
      });
    };

    const displayFilteredDataOnMap = (data) => {
      clearMapLayers();
      noDataFound.value = false;

      if (data.length > 0) {
        const item = data[0];
        const coordinates = item.State ? getStateCoordinates(item.State) : getTerritoryCoordinates(item.Territory);
        const fullName = item.State ? getFullStateName(item.State) : getFullTerritoryName(item.Territory);

        if (coordinates) {
          map.value.setView(coordinates, 6);

          const customIcon = L.divIcon({
            className: "custom-div-icon",
            html: "<div style='background-color:#6D2E46; width: 12px; height: 12px; border-radius: 50%;'></div>",
            iconSize: [12, 12],
            iconAnchor: [6, 6],
          });

          const marker = L.marker(coordinates, { icon: customIcon }).addTo(map.value);

          const popupContent = `
        <div class="custom-popup">
          <h3>${fullName}</h3>
          <p><strong>Prénom:</strong> ${item.Name}</p>
          <p><strong>Sexe:</strong> ${item.Sex === "M" ? "Masculin" : "Féminin"}</p>
          <p><strong>Année:</strong> ${item.Year}</p>
          <p><strong>Nombre:</strong> ${item.Count}</p>
        </div>
      `;

          marker.bindPopup(popupContent).openPopup();
        } else {
          console.error("Coordonnées non trouvées pour:", item.State || item.Territory);
        }
      } else {
        noDataFound.value = true;
      }

      filtersApplied.value = true;
    };

    const fetchAndDisplayData = async () => {
      const { selectedRegionType, region, year, sex, name } = props.filters;

      if (!selectedRegionType || !region || !year || !sex || !name) {
        filtersApplied.value = false;
        return;
      }

      try {
        const response = await fetch(`http://localhost:8000/api/names_data?region_type=${selectedRegionType}&region_name=${region}&year=${year}&sex=${sex}&name=${name}`);
        const data = await response.json();

        if (Array.isArray(data) && data.length > 0) {
          displayFilteredDataOnMap(data);
        } else {
          noDataFound.value = true;
          filtersApplied.value = true;
        }
      } catch (error) {
        console.error("Erreur lors de la récupération des données :", error);
        noDataFound.value = true;
        filtersApplied.value = true;
      }
    };

    onMounted(() => {
      initializeMap();
    });

    watch(
      () => props.filters,
      (newFilters, oldFilters) => {
        if (JSON.stringify(newFilters) !== JSON.stringify(oldFilters)) {
          nextTick(() => {
            if (!map.value) {
              initializeMap();
            }
            fetchAndDisplayData();
          });
        }
      },
      { deep: true }
    );

    return {
      mapContainer,
      filtersApplied,
      noDataFound,
      fetchAndDisplayData,
    };
  },
};
</script>

<style scoped>
.stats-diversity-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.map-overlay p {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

:deep(.custom-div-icon) {
  background: none;
  border: none;
}

:deep(.leaflet-popup-content-wrapper) {
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 3px 14px rgba(0, 0, 0, 0.4);
}

:deep(.leaflet-popup-content) {
  margin: 13px 19px;
  line-height: 1.4;
}

:deep(.custom-popup h3) {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
}

:deep(.custom-popup p) {
  margin: 0 0 5px 0;
  color: #666;
}

:deep(.custom-popup strong) {
  color: #333;
}
</style>
