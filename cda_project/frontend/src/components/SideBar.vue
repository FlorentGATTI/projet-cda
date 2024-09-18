<template>
  <v-navigation-drawer app class="sidebar-container">
    <v-list>
      <v-list-item>
        <v-list-item-title class="filter-title">Filtres généraux</v-list-item-title>
      </v-list-item>

      <v-list-item>
        <v-radio-group v-model="filters.selectedRegionType" row @change="resetFilters" aria-label="Type de région">
          <v-radio label="État" value="state"></v-radio>
          <v-radio label="Territoire" value="territory"></v-radio>
        </v-radio-group>
      </v-list-item>

      <v-list-item>
        <v-select v-model="filters.region" :items="mappedRegionList" :label="filters.selectedRegionType === 'state' ? 'États' : 'Territoires'" item-title="name" item-value="code" @update:model-value="updateYearList" :loading="loadingYears" aria-label="Sélection de la région"></v-select>
      </v-list-item>

      <v-list-item>
        <v-select v-model="filters.year" :items="yearList" :label="filters.selectedRegionType === 'state' ? 'Année (États)' : 'Année (Territoires)'" item-title="title" item-value="value" @update:model-value="updateSexList" :disabled="!filters.region" :loading="loadingSexes" aria-label="Sélection de l'année"></v-select>
      </v-list-item>

      <v-list-item>
        <v-select v-model="filters.sex" :items="sexList" label="Sexe" item-title="title" item-value="value" @update:model-value="enableNameSearch" :disabled="!filters.year" aria-label="Sélection du sexe"></v-select>
      </v-list-item>

      <v-list-item>
        <v-autocomplete
          v-model="filters.name"
          :items="nameList"
          :label="filters.selectedRegionType === 'state' ? 'Prénom (États)' : 'Prénom (Territoires)'"
          item-title="title"
          item-value="value"
          :loading="loadingNames"
          :disabled="!canSearchNames"
          @update:search="debouncedSearchNames"
          @update:model-value="onNameSelected"
          clearable
          hide-no-data
          hide-selected
          return-object
          aria-label="Recherche de prénom"
        ></v-autocomplete>
      </v-list-item>

      <v-list-item>
        <v-btn @click="applyFilters" color="primary" :disabled="!isFormValid" aria-label="Appliquer les filtres"> Appliquer les filtres </v-btn>
      </v-list-item>

      <v-list-item v-if="error">
        <v-alert type="error" dense>{{ error }}</v-alert>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { ref, computed, watch } from "vue";
import debounce from "lodash/debounce";
import { stateMapping, territoryMapping, getFullStateName, getFullTerritoryName } from "../../../data/stateTerritoryMappings";

const formatName = (name) => {
  return name
    .toLowerCase()
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
};

export default {
  name: "SideBar",
  emits: ["apply-filters"],
  setup(props, { emit }) {
    const filters = ref({
      selectedRegionType: "state",
      region: null,
      year: null,
      sex: null,
      name: null,
    });

    const yearList = ref([]);
    const sexList = ref([]);
    const nameList = ref([]);
    const loadingYears = ref(false);
    const loadingSexes = ref(false);
    const loadingNames = ref(false);
    const canSearchNames = ref(false);
    const error = ref(null);

    const mappedRegionList = computed(() => {
      const mapping = filters.value.selectedRegionType === "state" ? stateMapping : territoryMapping;
      return Object.entries(mapping).map(([code, name]) => ({ name, code }));
    });

    const isFormValid = computed(() => {
      return filters.value.region && filters.value.year && filters.value.sex && filters.value.name;
    });

    const resetFilters = () => {
      filters.value.region = null;
      filters.value.year = null;
      filters.value.sex = null;
      filters.value.name = null;
      yearList.value = [];
      sexList.value = [];
      nameList.value = [];
      canSearchNames.value = false;
      error.value = null;
    };

    const updateYearList = async () => {
      if (!filters.value.region) return;
      loadingYears.value = true;
      try {
        const endpoint = filters.value.selectedRegionType === "state" ? "distinct_years_states" : "distinct_years_territories";
        const response = await fetch(`http://localhost:8000/api/${endpoint}?region=${filters.value.region}`);
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          yearList.value = data.map((year) => ({ title: year.toString(), value: year }));
        } else {
          error.value = "Aucune année disponible pour cette région.";
          yearList.value = [];
        }
      } catch (err) {
        error.value = `Erreur lors du chargement des années: ${err.message}`;
        yearList.value = [];
      } finally {
        loadingYears.value = false;
      }
    };

    const updateSexList = async () => {
      if (!filters.value.region || !filters.value.year) return;
      loadingSexes.value = true;
      try {
        const response = await fetch(`http://localhost:8000/api/distinct_sexes?region_type=${filters.value.selectedRegionType}&region=${filters.value.region}&year=${filters.value.year}`);
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          sexList.value = data.map((sex) => ({
            title: sex === "M" ? "Masculin" : "Féminin",
            value: sex,
          }));
        } else {
          error.value = "Aucune donnée de sexe disponible pour cette sélection.";
          sexList.value = [];
        }
      } catch (err) {
        error.value = `Erreur lors du chargement des sexes: ${err.message}`;
        sexList.value = [];
      } finally {
        loadingSexes.value = false;
      }
    };

    const enableNameSearch = () => {
      canSearchNames.value = !!filters.value.region && !!filters.value.year && !!filters.value.sex;
    };

    const searchNames = async (search) => {
      if (!canSearchNames.value || !search) {
        nameList.value = [];
        return;
      }
      loadingNames.value = true;
      try {
        const response = await fetch(`http://localhost:8000/api/names_data?region_type=${filters.value.selectedRegionType}&region_name=${filters.value.region}&year=${filters.value.year}&sex=${filters.value.sex}&name=${search}`);
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          nameList.value = data.map((item) => ({ title: item.Name, value: item.Name }));
        } else {
          nameList.value = [];
        }
        error.value = null;
      } catch (err) {
        console.error("Erreur lors de la recherche des prénoms:", err);
        error.value = `Erreur lors de la recherche des prénoms: ${err.message}`;
        nameList.value = [];
      } finally {
        loadingNames.value = false;
      }
    };

    const debouncedSearchNames = debounce(searchNames, 300);

    const onNameSelected = (selectedName) => {
      if (selectedName) {
        filters.value.name = selectedName.value;
      } else {
        filters.value.name = null;
      }
    };

    const applyFilters = () => {
      if (isFormValid.value) {
        const fullRegionName = filters.value.selectedRegionType === "state" ? getFullStateName(filters.value.region) : getFullTerritoryName(filters.value.region);

        const appliedFilters = {
          selectedRegionType: filters.value.selectedRegionType,
          region: filters.value.region,
          regionName: fullRegionName,
          year: filters.value.year,
          sex: filters.value.sex,
          name: formatName(filters.value.name),
        };

        emit("apply-filters", appliedFilters);
      } else {
        error.value = "Veuillez remplir tous les champs avant d'appliquer les filtres.";
      }
    };

    watch(() => filters.value.selectedRegionType, resetFilters);

    watch(
      () => filters.value.year,
      (newYear) => {
        if (newYear) {
          updateSexList();
        }
      }
    );

    watch(
      () => filters.value.sex,
      (newSex) => {
        if (newSex) {
          enableNameSearch();
        }
      }
    );

    watch(
      () => filters.value.region,
      (newRegion) => {
        if (newRegion) {
          updateYearList();
        } else {
          yearList.value = [];
        }
      }
    );

    return {
      filters,
      mappedRegionList,
      yearList,
      sexList,
      nameList,
      loadingYears,
      loadingSexes,
      loadingNames,
      canSearchNames,
      isFormValid,
      error,
      resetFilters,
      updateYearList,
      updateSexList,
      enableNameSearch,
      debouncedSearchNames,
      onNameSelected,
      applyFilters,
    };
  },
};
</script>

<style scoped>
.sidebar-container {
  background: #e1d7cd;
  padding: 10px;
}

.filter-title {
  font-weight: bold;
  font-size: 1.2em;
  margin-bottom: 10px;
}
</style>
