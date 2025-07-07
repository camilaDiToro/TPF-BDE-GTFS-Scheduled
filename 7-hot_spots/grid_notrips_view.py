import geopandas as gpd
import folium as f
import branca.colormap as cm
from folium.features import GeoJsonTooltip
from db_utils.db_connection import get_engine

def load_grid_100m(engine):
    query = """
    SELECT grid_id, notrips, routes, ST_Transform(geom, 4326) AS geometry
    FROM brooklyn.grid_500m_32118;
    """
    return gpd.read_postgis(query, engine, geom_col='geometry')

def load_brooklyn_boundary(engine):
    query = """
    SELECT ST_Transform(geom_32118, 4326) AS geometry
    FROM public.ny_adm
    WHERE boroname = 'Brooklyn';
    """
    return gpd.read_postgis(query, engine, geom_col='geometry')

def visualize_grid(grid_gdf, brooklyn_boundary, cutoff=500):
    transport_map = f.Map(location=[40.65, -73.95], tiles='CartoDB positron', zoom_start=11)

    # Colormap for notrips
    colormap = cm.LinearColormap(
        colors=['white', 'yellow', 'orange', 'red', 'darkred'],
        vmin=0,
        vmax=cutoff,
        caption='Trip Count'
    )
    colormap.add_to(transport_map)

    # --- Borde de Brooklyn ---
    for _, row in brooklyn_boundary.iterrows():
        geojson = f.GeoJson(
            data={
                "type": "Feature",
                "geometry": row['geometry'].__geo_interface__,
                "properties": {}
            },
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'purple',
                'weight': 2,
                'fillOpacity': 0.0,
                'opacity': 0.7
            }
        )
        geojson.add_to(transport_map)

    # --- Cuadrículas coloreadas según notrips ---
    for _, row in grid_gdf.iterrows():
        trip_count = min(row['notrips'], cutoff)
        color = colormap(trip_count)

        geo_json = f.GeoJson(
            data={
                "type": "Feature",
                "geometry": row['geometry'].__geo_interface__,
                "properties": {
                    "grid_id": row['grid_id'],
                    "notrips": row['notrips'],
                    "routes": row['routes']
                }
            },
            style_function=lambda x, color=color: {
                'fillColor': color,
                'color': 'grey',
                'weight': 0.5,
                'fillOpacity': 0.6,
                'opacity': 0.3
            },
            tooltip=GeoJsonTooltip(
                fields=['grid_id', 'notrips', 'routes'],
                aliases=['Grid ID', 'Trip Count', 'Routes'],
                localize=True
            )
        )
        geo_json.add_to(transport_map)

    return transport_map

# --- MAIN ---
if __name__ == "__main__":
    engine = get_engine()
    grid_gdf = load_grid_100m(engine)
    brooklyn_boundary = load_brooklyn_boundary(engine)
    grid_map = visualize_grid(grid_gdf, brooklyn_boundary)
    grid_map.save("outputs/grid_notrips_500m.html")
    print("Mapa guardado como 'grid_notrips_100m.html'")
