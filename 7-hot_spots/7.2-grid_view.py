import geopandas as gpd
import folium as f
from db_utils.db_connection import get_engine

def load_grid_100m(engine):
    query = """
    SELECT grid_id, ST_Transform(geom, 4326) AS geometry
    FROM brooklyn.grid_100m_32118;
    """
    return gpd.read_postgis(query, engine, geom_col='geometry')

def visualize_grid(grid_gdf):
    transport_map = f.Map(location=[40.65, -73.95], tiles='CartoDB positron', zoom_start=12)

    for _, row in grid_gdf.iterrows():
        geojson = f.GeoJson(
            data={
                "type": "Feature",
                "geometry": row['geometry'].__geo_interface__,
                "properties": {"grid_id": row["grid_id"]}
            },
            style_function=lambda x: {
                'fillColor': '#0080ff',
                'color': '#004080',
                'weight': 1,
                'fillOpacity': 0.2,
                'opacity': 0.5
            },
            tooltip=f"Grid ID: {row['grid_id']}"
        )
        geojson.add_to(transport_map)

    return transport_map

# --- MAIN ---
if __name__ == "__main__":
    engine = get_engine()
    grid_gdf = load_grid_100m(engine)
    grid_map = visualize_grid(grid_gdf)
    grid_map.save("outputs/grid_100m.html")
    print("Mapa guardado como 'grid_100m.html'")