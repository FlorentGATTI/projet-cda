<template>
  <v-navigation-drawer app class="sidebar-container" :class="{ 'sidebar-mobile': !isDesktop }">
    <v-list class="pa-4">
      <v-list-item class="mb-6 mt-4">
        <v-btn-toggle v-model="filters.selectedType" mandatory class="d-flex w-100">
          <v-btn value="state" class="flex-grow-1 custom-toggle-btn">
            <v-icon size="small" class="mr-1">mdi-map-marker</v-icon>
            <span class="button-text">État</span>
          </v-btn>
          <v-btn value="territory" class="flex-grow-1 custom-toggle-btn">
            <v-icon size="small" class="mr-1">mdi-earth</v-icon>
            <span class="button-text">Territoire</span>
          </v-btn>
        </v-btn-toggle>
      </v-list-item>

      <v-select v-model="filters.selectedValue" :items="mappedList" :label="filters.selectedType === 'state' ? 'États' : 'Territoires'" variant="plain" hide-details dense item-title="name" item-value="code" @update:model-value="updateYearList" :loading="loadingYears" :disabled="isLoading" prepend-icon="mdi-map" class="mb-6 centered-input"></v-select>

      <v-select v-model="filters.year" :items="yearList" :label="filters.selectedType === 'state' ? 'Année (États)' : 'Année (Territoires)'" variant="plain" hide-details dense item-title="title" item-value="value" @update:model-value="updateSexList" :disabled="!filters.selectedValue || isLoading" :loading="loadingSexes" prepend-icon="mdi-calendar" class="mb-6 centered-input"></v-select>

      <v-select v-model="filters.sex" :items="sexList" label="Sexe" variant="plain" hide-details dense item-title="title" item-value="value" @update:model-value="enableNameSearch" :disabled="!filters.year || isLoading" prepend-icon="mdi-gender-male-female" class="mb-6 centered-input"></v-select>

      <v-autocomplete
        v-model="filters.name"
        :items="nameList"
        :label="filters.selectedType === 'state' ? 'Prénom (États)' : 'Prénom (Territoires)'"
        variant="plain"
        hide-details
        dense
        item-title="title"
        item-value="value"
        :loading="loadingNames"
        :disabled="!canSearchNames || isLoading"
        @update:search="debouncedSearchNames"
        @update:model-value="onNameSelected"
        :error-messages="nameError"
        clearable
        hide-no-data
        hide-selected
        return-object
        prepend-icon="mdi-account"
        class="mb-8 centered-input"
      ></v-autocomplete>

      <v-btn @click="applyFilters" color="primary" :disabled="!isFormValid || isLoading" block class="mb-4">
        <v-icon left>mdi-magnify</v-icon>
        {{ isLoading ? "Chargement..." : "Rechercher" }}
      </v-btn>

      <v-btn @click="resetAllFilters" color="secondary" block outlined>
        <v-icon left>mdi-refresh</v-icon>
        Réinitialiser
      </v-btn>

      <v-alert v-if="error" type="error" dense class="mt-4">{{ error }}</v-alert>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import { ref, computed, watch } from "vue";
import debounce from "lodash/debounce";
import { stateMapping, territoryMapping, getFullStateName, getFullTerritoryName } from "../../../data/stateTerritoryMappings";
import { useDisplay } from "vuetify";

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
  props: {
    isLoading: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    const { lgAndUp } = useDisplay();
    const isDesktop = computed(() => lgAndUp.value);

    const filters = ref({
      selectedType: "state",
      selectedValue: null,
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
    const nameError = ref("");

    const mappedList = computed(() => {
      const mapping = filters.value.selectedType === "state" ? stateMapping : territoryMapping;
      return Object.entries(mapping).map(([code, name]) => ({ name, code }));
    });

    const isFormValid = computed(() => {
      return filters.value.selectedValue && filters.value.year && filters.value.sex && filters.value.name;
    });

    const isReady = computed(() => {
      return mappedList.value.length > 0;
    });

    const resetFilters = () => {
      filters.value = {
        selectedType: filters.value.selectedType,
        selectedValue: null,
        year: null,
        sex: null,
        name: null,
      };
      yearList.value = [];
      sexList.value = [];
      nameList.value = [];
      canSearchNames.value = false;
      error.value = null;
      nameError.value = "";
    };

    const resetAllFilters = () => {
      filters.value.selectedType = "state";
      resetFilters();
    };

    const updateYearList = async () => {
      if (!filters.value.selectedValue) return;
      loadingYears.value = true;
      error.value = null;
      try {
        const endpoint = filters.value.selectedType === "state" ? "distinct_years_states" : "distinct_years_territories";
        const response = await fetch(`http://localhost:8000/api/${endpoint}?${filters.value.selectedType}=${filters.value.selectedValue}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          yearList.value = data.map((year) => ({ title: year.toString(), value: year }));
        } else {
          error.value = `Aucune année disponible pour ${filters.value.selectedType === "state" ? "cet état" : "ce territoire"}.`;
          yearList.value = [];
        }
      } catch (err) {
        console.error("Error fetching years:", err);
        error.value = `Erreur lors du chargement des années: ${err.message}`;
        yearList.value = [];
      } finally {
        loadingYears.value = false;
      }
    };

    const updateSexList = async () => {
      if (!filters.value.selectedValue || !filters.value.year) return;
      loadingSexes.value = true;
      error.value = null;
      try {
        const response = await fetch(`http://localhost:8000/api/distinct_sexes?selected_type=${filters.value.selectedType}&${filters.value.selectedType}=${filters.value.selectedValue}&year=${filters.value.year}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
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
        console.error("Error fetching sexes:", err);
        error.value = `Erreur lors du chargement des sexes: ${err.message}`;
        sexList.value = [];
      } finally {
        loadingSexes.value = false;
      }
    };

    const enableNameSearch = () => {
      canSearchNames.value = !!filters.value.selectedValue && !!filters.value.year && !!filters.value.sex;
    };

    const searchNames = async (search) => {
      if (!canSearchNames.value || !search || search.length < 2) {
        nameList.value = [];
        nameError.value = search && search.length < 2 ? "Entrez au moins 2 caractères" : "";
        return;
      }
      loadingNames.value = true;
      nameError.value = "";
      try {
        const url = `http://localhost:8000/api/names_data?selected_type=${filters.value.selectedType}&${filters.value.selectedType}=${filters.value.selectedValue}&year=${filters.value.year}&sex=${filters.value.sex}&name=${search}`;
        console.log("Fetching URL:", url);
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (Array.isArray(data) && data.length > 0) {
          nameList.value = data.map((item) => ({ title: item.Name, value: item.Name }));
        } else {
          nameList.value = [];
          nameError.value = "Aucun prénom trouvé";
        }
      } catch (err) {
        console.error("Error searching names:", err);
        nameError.value = "Erreur lors de la recherche des prénoms";
        nameList.value = [];
      } finally {
        loadingNames.value = false;
      }
    };

    const debouncedSearchNames = debounce(searchNames, 300);

    const onNameSelected = (selectedName) => {
      if (selectedName) {
        filters.value.name = selectedName.value;
        nameError.value = "";
      } else {
        filters.value.name = null;
      }
    };

    const applyFilters = () => {
      if (isFormValid.value && !props.isLoading) {
        const fullName = filters.value.selectedType === "state" ? getFullStateName(filters.value.selectedValue) : getFullTerritoryName(filters.value.selectedValue);

        const appliedFilters = {
          selectedType: filters.value.selectedType,
          selectedValue: filters.value.selectedValue,
          fullName: fullName,
          year: filters.value.year,
          sex: filters.value.sex,
          name: formatName(filters.value.name),
        };

        emit("apply-filters", appliedFilters);
      } else {
        error.value = "Veuillez remplir tous les champs avant d'appliquer les filtres.";
      }
    };

    watch(() => filters.value.selectedType, resetFilters);

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
      () => filters.value.selectedValue,
      (newValue) => {
        if (newValue) {
          updateYearList();
        } else {
          yearList.value = [];
        }
      }
    );

    return {
      filters,
      mappedList,
      yearList,
      sexList,
      nameList,
      loadingYears,
      loadingSexes,
      loadingNames,
      canSearchNames,
      isFormValid,
      error,
      isDesktop,
      isReady,
      resetFilters,
      resetAllFilters,
      updateYearList,
      updateSexList,
      enableNameSearch,
      nameError,
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
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.sidebar-mobile {
  height: 100%;
  position: fixed;
  top: 64px;
  left: 0;
  bottom: 0;
  width: 250px;
  z-index: 1000;
}

.v-btn {
  text-transform: none;
}

.v-list-item {
  transition: all 0.3s ease;
}

.v-btn-toggle {
  justify-content: space-between;
  width: 100%;
}

.v-btn-toggle .v-btn {
  flex-grow: 1;
}

.centered-input :deep(.v-field__input) {
  font-size: 18px !important;
}

.centered-input :deep(.v-select__selection) {
  font-size: 18px !important;
}

.centered-input :deep(.v-label) {
  font-size: 18px !important;
  width: 100%;
}

.centered-input :deep(.v-input__prepend) {
  margin-right: auto !important;
}

.centered-input :deep(.v-input__append) {
  margin-left: auto !important;
}

:deep(.v-field) {
  border-color: transparent !important;
  background-color: transparent !important;
  box-shadow: none !important;
  padding-top: 12px !important;
  padding-bottom: 12px !important;
}

:deep(.v-field__outline) {
  --v-field-border-width: 0 !important;
  border: none !important;
  opacity: 0 !important;
}

:deep(.v-field__input) {
  min-height: 32px !important;
  padding-top: 0 !important;
  border: none !important;
  font-size: 16px !important; /* Augmentation de la taille de la police */
  text-align: center !important; /* Centrage du texte */
}

:deep(.v-select__selection) {
  margin-top: 0 !important;
  font-size: 16px !important; /* Augmentation de la taille de la police */
}

:deep(.v-field__input::before),
:deep(.v-field__input::after) {
  border: none !important;
  background: none !important;
  left: 10px;
  top: 5px;
}

:deep(.v-field__input) {
  left: 10px;
  top: 5px;
}

:deep(.v-label) {
  top: 8px !important;
  left: 10px;
  font-size: 16px !important;
}

:deep(.v-field:hover),
:deep(.v-field--focused) {
  background-color: rgba(0, 0, 0, 0.03) !important;
}

:deep(.v-field),
:deep(.v-select),
:deep(.v-text-field) {
  border: none !important;
  outline: none !important;
}

:deep(.v-field input) {
  border: none !important;
  background-color: transparent !important;
  outline: none !important;
  text-align: center !important;
}

:deep(.v-input__prepend) {
  margin-right: 8px !important;
}
:deep(.v-btn) {
  font-size: 16px !important;
}

.custom-toggle-btn {
  font-size: 0.85rem !important;
  padding: 0 8px !important;
  height: 46px !important;
}

.custom-toggle-btn .v-btn__content {
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.button-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.mb-6 {
  margin-bottom: 20px !important;
}
</style>
