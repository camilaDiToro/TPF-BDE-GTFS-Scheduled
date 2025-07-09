import geopandas as gpd
import folium as f
import branca.colormap as cm
from folium.features import GeoJsonTooltip
from db_utils.db_connection import get_engine

def load_geom_boundary(engine):
    query = """
    SELECT geom as geometry
    FROM public.ny_adm
    WHERE boroname = 'Brooklyn';
    """
    return gpd.read_postgis(query, engine, geom_col='geometry')

def load_segments_from_postgis(engine):
    query = """
    SELECT * FROM brooklyn.segments_load;
    """
    return gpd.read_postgis(query, engine, geom_col='geometry')

def visualize(segment_data, brooklyn_boundary=None, cutoff=20000):
    transport_map = f.Map(location=[40.65, -73.95], tiles='CartoDB positron', zoom_start=11)

    colormap = cm.LinearColormap(
        colors=['white', 'yellow', 'orange', 'red', 'darkred'],
        vmin=0,
        vmax=cutoff,
        caption='Trip Count'
    )
    colormap.add_to(transport_map)

    # --- Agregar geometría de Brooklyn al fondo ---
    if brooklyn_boundary is not None:
        for _, row in brooklyn_boundary.iterrows():
            geojson = f.GeoJson(
                data={
                    "type": "Feature",
                    "geometry": row['geometry'].__geo_interface__,
                    "properties": {},
                },
                style_function=lambda x: {
                    'fillColor': 'purple',
                    'color': 'purple',
                    'weight': 2,
                    'fillOpacity': 0.1,
                    'opacity': 0.4
                }
            )
            geojson.add_to(transport_map)

    # --- Agregar segmentos ---
    for _, segment in segment_data.iterrows():
        trip_count = min(segment['notrips'], cutoff)
        color = colormap(trip_count)
        geo_json = f.GeoJson(
            data={
                "type": "Feature",
                "geometry": segment['geometry'].__geo_interface__,
                "properties": {
                    "routes": segment['routes'],
                    "from_stop_name": segment['from_stop_name'],
                    "to_stop_name": segment['to_stop_name'],
                    "notrips": segment['notrips']
                }
            },
            style_function=lambda x, color=color: {
                'color': color, 'weight': 3, 'opacity': 0.7
            },
            tooltip=GeoJsonTooltip(
                fields=['routes', 'from_stop_name', 'to_stop_name', 'notrips'],
                aliases=['Routes', 'From Stop', 'To Stop', 'Trip Count'],
                localize=True
            )
        )
        geo_json.add_to(transport_map)

    return transport_map

# --- MAIN ---
if __name__ == "__main__":
    engine = get_engine()
    segment_gdf = load_segments_from_postgis(engine)
    geom_boundary = load_geom_boundary(engine).to_crs(epsg=4326)
    transport_map = visualize(segment_gdf, geom_boundary)
    transport_map.save("outputs/segments_partial_brooklyn_map.html")
    print("Mapa guardado como 'segments_partial_brooklyn_map.html'")
