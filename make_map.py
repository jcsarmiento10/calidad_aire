# JC
# https://github.com/bertcarremans/air_pollution_forecasting/blob/master/notebooks/Visualizing%20Air%20Pollution%20in%20Belgium.ipynb

import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

def create_geojson_features(df):
    features = []
    for _, row in df.iterrows():
        feature = {
            'type': 'Feature',
            'geometry': {
                'type':'Point', 
                'coordinates':[row['Longitud'],row['Latitud']]
            },
            'properties': {
                'time': row['DatetimeBegin'].date().__str__(),
                'style': {'color' : row['color']}, # revisar que usar
                'icon': 'circle',
                'iconstyle':{
                    'fillColor': row['color'],
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 7
                }
            }
        }
        features.append(feature)
    return features


df = pd.read_csv('data.csv')
# esperar que hace santi para diferenciar IDs
variables = []

# revisar location y tipo de mapa
basemap = folium.Map(location=[37.43, -122.17], zoom_start=6, tiles="Stamen Terrain") 

for var in variables:
    df_filtered = filter(df, var) # not real
    geo_features = create_geojson_features(df_filtered)
    TimestampedGeoJson({'type': 'FeatureCollection', 'features': geo_features}, period='P1M', #revisar P1M
                       add_last_point=True, auto_play=False, loop=False, max_speed=1, 
                       loop_button=True, date_options='YYYY/MM', duration='P1M',
                       time_slider_drag_update=True).add_to(basemap)
    
basemap.add_child(folium.LayerControl())

basemap.save("Map1.html")
