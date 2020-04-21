# JC
# https://github.com/bertcarremans/air_pollution_forecasting/blob/master/notebooks/Visualizing%20Air%20Pollution%20in%20Belgium.ipynb

import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson
import preprocessing as pre
from bokeh.palettes import RdYlBu
from tqdm import tqdm

def create_geojson_features(df):
    features = []
    for _, row in tqdm(df.iterrows()):
        feature = {
            'type': 'Feature',
            'geometry': {
                'type':'Point', 
                'coordinates':[row['Longitud'],row['Latitud']]
            },
            'properties': {
                'time': row['Fecha'].date().__str__(),
                'style': {'color' : row['color']},
                'icon': 'circle',
                'iconstyle':{
                    'fillColor': row['color'],
                    'fillOpacity': 0.8,
                    'stroke': 'true',
                    'radius': 5
                }
            }
        }
        features.append(feature)
    return features

data = pre.read_data()

variables = data['Variable'].unique().tolist()[:2] # Probando solo con dos
basemap = folium.Map(location=[4.71, -74.07], zoom_start=6, tiles="Stamen Terrain") # revisar tiles

for var in variables:
    print(var)
    df_variable = pre.df_variable(data, var)
    # add color column    
    df_variable['color'] = [RdYlBu[11][val] for val in pd.cut(x=df_variable['Concentración'], 
                                                              bins=11, labels=False)]
    
    
    geo_features = create_geojson_features(df_variable.reset_index())
    basemap.add_child(TimestampedGeoJson({'type': 'FeatureCollection', 'features': geo_features}, 
                                    period='P1D', add_last_point=True, auto_play=False, loop=False, 
                                    max_speed=10, loop_button=True, date_options='YYYY/MM', 
                                    duration='P1M', time_slider_drag_update=True))
    
basemap.add_child(folium.LayerControl())

basemap.save("Map2.html")
