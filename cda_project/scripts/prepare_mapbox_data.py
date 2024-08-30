import os
import json
from pymongo import MongoClient

def connect_to_mongodb():
    client = MongoClient("mongodb://localhost:27017")
    db = client["cda"]
    return db

def transform_data_to_geojson(collection, state_coordinates):
    features = []
    for record in collection.find():
        state = record['State'] if 'State' in record else record['Territory']
        if state not in state_coordinates:
            continue

        coordinates = state_coordinates[state]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coordinates
            },
            "properties": {
                "State": state,
                "Name": record['Name'],
                "Sex": record['Sex'],
                "Year": record['Year'],
                "Count": record['Count']
            }
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    return geojson

def save_geojson(geojson, filename):
    with open(filename, 'w') as f:
        json.dump(geojson, f)

def main():
    db = connect_to_mongodb()
    
    state_coordinates = {
    "AL": [-86.9023, 32.3182],  # Alabama
    "AK": [-154.4931, 63.5888],  # Alaska
    "AZ": [-111.0937, 34.0489],  # Arizona
    "AR": [-92.3731, 34.9697],   # Arkansas
    "CA": [-119.4179, 36.7783],  # California
    "CO": [-105.7821, 39.5501],  # Colorado
    "CT": [-72.7554, 41.6032],   # Connecticut
    "DE": [-75.5277, 38.9108],   # Delaware
    "FL": [-81.5158, 27.6648],   # Florida
    "GA": [-82.9071, 32.1656],   # Georgia
    "HI": [-155.5828, 19.8968],  # Hawaii
    "ID": [-114.7420, 44.0682],  # Idaho
    "IL": [-89.3985, 40.6331],   # Illinois
    "IN": [-86.1349, 40.2672],   # Indiana
    "IA": [-93.0977, 41.8780],   # Iowa
    "KS": [-98.4842, 39.0119],   # Kansas
    "KY": [-84.2700, 37.8393],   # Kentucky
    "LA": [-91.9623, 30.9843],   # Louisiana
    "ME": [-69.4455, 45.2538],   # Maine
    "MD": [-76.6413, 39.0458],   # Maryland
    "MA": [-71.3824, 42.4072],   # Massachusetts
    "MI": [-85.6024, 44.3148],   # Michigan
    "MN": [-94.6859, 46.7296],   # Minnesota
    "MS": [-89.3985, 32.3547],   # Mississippi
    "MO": [-91.8318, 37.9643],   # Missouri
    "MT": [-110.3626, 46.8797],  # Montana
    "NE": [-99.9018, 41.4925],   # Nebraska
    "NV": [-116.4194, 38.8026],  # Nevada
    "NH": [-71.5724, 43.1939],   # New Hampshire
    "NJ": [-74.4057, 40.0583],   # New Jersey
    "NM": [-105.8701, 34.5199],  # New Mexico
    "NY": [-74.0060, 40.7128],   # New York
    "NC": [-79.0193, 35.7596],   # North Carolina
    "ND": [-101.0020, 47.5515],  # North Dakota
    "OH": [-82.9071, 40.4173],   # Ohio
    "OK": [-97.5164, 35.0078],   # Oklahoma
    "OR": [-120.5542, 43.8041],  # Oregon
    "PA": [-77.1945, 41.2033],   # Pennsylvania
    "RI": [-71.4774, 41.5801],   # Rhode Island
    "SC": [-81.1637, 33.8361],   # South Carolina
    "SD": [-99.9018, 43.9695],   # South Dakota
    "TN": [-86.5804, 35.5175],   # Tennessee
    "TX": [-99.9018, 31.9686],   # Texas
    "UT": [-111.0937, 39.3200],  # Utah
    "VT": [-72.5778, 44.5588],   # Vermont
    "VA": [-78.6569, 37.4316],   # Virginia
    "WA": [-120.7401, 47.7511],  # Washington
    "WV": [-80.4549, 38.5976],   # West Virginia
    "WI": [-89.6165, 43.7844],   # Wisconsin
    "WY": [-107.2903, 43.0759],  # Wyoming
    "DC": [-77.0369, 38.9072],   # Washington D.C.
    "PR": [-66.5901, 18.2208],   # Puerto Rico
    "GU": [144.7937, 13.4443],   # Guam
    "VI": [-64.8963, 18.3358],   # Virgin Islands
    "AS": [-170.1322, -14.2710], # American Samoa
    "MP": [145.7064, 15.0979],   # Northern Mariana Islands
}

    # Transformer les données des prénoms par état en GeoJSON
    names_by_state_collection = db["names_by_state"]
    geojson_state = transform_data_to_geojson(names_by_state_collection, state_coordinates)
    save_geojson(geojson_state, "data/names_by_state.geojson")

    # Transformer les données des prénoms par territoire en GeoJSON
    names_by_territory_collection = db["names_by_territory"]
    geojson_territory = transform_data_to_geojson(names_by_territory_collection, state_coordinates)
    save_geojson(geojson_territory, "data/names_by_territory.geojson")

    print("GeoJSON files have been created successfully.")

if __name__ == "__main__":
    main()
