export const stateMapping = {
  AK: "Alaska",
  AL: "Alabama",
  AR: "Arkansas",
  AZ: "Arizona",
  CA: "California",
  CO: "Colorado",
  CT: "Connecticut",
  DC: "District of Columbia",
  DE: "Delaware",
  FL: "Florida",
  GA: "Georgia",
  HI: "Hawaii",
  IA: "Iowa",
  ID: "Idaho",
  IL: "Illinois",
  IN: "Indiana",
  KS: "Kansas",
  KY: "Kentucky",
  LA: "Louisiana",
  MA: "Massachusetts",
  MD: "Maryland",
  ME: "Maine",
  MI: "Michigan",
  MN: "Minnesota",
  MO: "Missouri",
  MS: "Mississippi",
  MT: "Montana",
  NC: "North Carolina",
  ND: "North Dakota",
  NE: "Nebraska",
  NH: "New Hampshire",
  NJ: "New Jersey",
  NM: "New Mexico",
  NV: "Nevada",
  NY: "New York",
  OH: "Ohio",
  OK: "Oklahoma",
  OR: "Oregon",
  PA: "Pennsylvania",
  RI: "Rhode Island",
  SC: "South Carolina",
  SD: "South Dakota",
  TN: "Tennessee",
  TX: "Texas",
  UT: "Utah",
  VA: "Virginia",
  VT: "Vermont",
  WA: "Washington",
  WI: "Wisconsin",
  WV: "West Virginia",
  WY: "Wyoming",
};

export const territoryMapping = {
  PR: "Puerto Rico",
  TR: "Trust Territories", // "TR" est une abréviation générique, il peut s'agir des Territoires sous Tutelle
};

export const stateCoordinates = {
  AK: [61.3707, -152.4044], // Alaska
  AL: [32.8067, -86.7911], // Alabama
  AR: [34.9697, -92.3731], // Arkansas
  AZ: [33.7298, -111.4312], // Arizona
  CA: [36.1162, -119.6816], // California
  CO: [39.0598, -105.3111], // Colorado
  CT: [41.5978, -72.7554], // Connecticut
  DC: [38.8974, -77.0365], // District of Columbia
  DE: [39.3185, -75.5071], // Delaware
  FL: [27.7663, -81.6868], // Florida
  GA: [33.0406, -83.6431], // Georgia
  HI: [21.0943, -157.4983], // Hawaii
  IA: [42.0115, -93.2105], // Iowa
  ID: [44.2405, -114.4788], // Idaho
  IL: [40.3495, -88.9861], // Illinois
  IN: [39.8494, -86.2583], // Indiana
  KS: [38.5266, -96.7265], // Kansas
  KY: [37.6681, -84.6701], // Kentucky
  LA: [31.1695, -91.8678], // Louisiana
  MA: [42.2302, -71.5301], // Massachusetts
  MD: [39.0639, -76.8021], // Maryland
  ME: [44.6939, -69.3819], // Maine
  MI: [43.3266, -84.5361], // Michigan
  MN: [45.6945, -93.9002], // Minnesota
  MO: [38.4561, -92.2884], // Missouri
  MS: [32.7416, -89.6787], // Mississippi
  MT: [46.9219, -110.4544], // Montana
  NC: [35.6301, -79.8064], // North Carolina
  ND: [47.5289, -99.784], // North Dakota
  NE: [41.1254, -98.2681], // Nebraska
  NH: [43.4525, -71.5639], // New Hampshire
  NJ: [40.2989, -74.521], // New Jersey
  NM: [34.8405, -106.2485], // New Mexico
  NV: [38.3135, -117.0554], // Nevada
  NY: [42.1657, -74.9481], // New York
  OH: [40.3888, -82.7649], // Ohio
  OK: [35.5653, -96.9289], // Oklahoma
  OR: [44.572, -122.0709], // Oregon
  PA: [40.5908, -77.2098], // Pennsylvania
  RI: [41.6809, -71.5118], // Rhode Island
  SC: [33.8569, -80.945], // South Carolina
  SD: [44.2998, -99.4388], // South Dakota
  TN: [35.7478, -86.6923], // Tennessee
  TX: [31.0545, -97.5635], // Texas
  UT: [40.15, -111.8624], // Utah
  VA: [37.7693, -78.17], // Virginia
  VT: [44.0459, -72.7107], // Vermont
  WA: [47.4009, -121.4905], // Washington
  WI: [44.2685, -89.6165], // Wisconsin
  WV: [38.4912, -80.9545], // West Virginia
  WY: [42.7559, -107.3025], // Wyoming
};

export const territoryCoordinates = {
  PR: [18.2208, -66.5901], // Puerto Rico
  TR: [7.5, 134.5], // Trust Territories (approximated)
};

// Fonction pour obtenir le nom complet d'un État
export function getFullStateName(abbreviation) {
  return stateMapping[abbreviation] || abbreviation;
}

// Fonction pour obtenir le nom complet d'un Territoire
export function getFullTerritoryName(abbreviation) {
  return territoryMapping[abbreviation] || abbreviation;
}

// Fonction pour obtenir les coordonnées d'un État
export function getStateCoordinates(state) {
  return stateCoordinates[state] || [37.8, -96]; // Coordonnées par défaut (USA)
}

// Fonction pour obtenir les coordonnées d'un Territoire
export function getTerritoryCoordinates(territory) {
  return territoryCoordinates[territory] || [37.8, -96]; // Coordonnées par défaut (USA)
}
