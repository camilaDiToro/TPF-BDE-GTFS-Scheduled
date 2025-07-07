import geopandas as gpd
import folium as f
import seaborn as sns
from folium.features import GeoJsonTooltip
from db_utils.db_connection import get_engine


def load_brooklyn_boundary(engine):
    query = """
    SELECT geom as geometry
    FROM public.ny_adm
    WHERE boroname = 'Brooklyn';
    """
    return gpd.read_postgis(query, engine, geom_col='geometry')


def load_hot_spot_routes(engine):
    query = """
    SELECT *
    FROM brooklyn.hot_spot_routes
    ORDER BY route_id;
    """
    return gpd.read_postgis(query, engine, geom_col='shape_geom')


def create_routes_map(routes_gdf, brooklyn_boundary=None):
    base_map = f.Map(location=[40.65, -73.95], tiles='CartoDB positron', zoom_start=11)

    # --- Brooklyn boundary ---
    if brooklyn_boundary is not None:
        boundary_group = f.FeatureGroup(name="Brooklyn Boundary", show=True)
        for _, row in brooklyn_boundary.iterrows():
            f.GeoJson(
                data=row['geometry'].__geo_interface__,
                style_function=lambda x: {
                    'fillColor': 'purple',
                    'color': 'purple',
                    'weight': 2,
                    'fillOpacity': 0.1,
                    'opacity': 0.4
                }
            ).add_to(boundary_group)
        boundary_group.add_to(base_map)

    # --- Color por route_id con Set3 ---
    route_ids = routes_gdf['route_id'].unique()
    color_palette = sns.color_palette("Set3", len(route_ids)).as_hex()
    color_map = dict(zip(route_ids, color_palette))

    # --- Group by shape_id ---
    route_count = 0
    for shape_id, shape_group in routes_gdf.groupby('shape_id'):
        route_id = shape_group['route_id'].iloc[0]
        route_name = shape_group['route_short_name'].iloc[0]
        direction = shape_group['direction_id'].iloc[0]
        color = color_map.get(route_id, 'black')

        layer_name = f"{route_name} (dir: {direction}, shape_id: {shape_id})"
        feature_group = f.FeatureGroup(name=layer_name, show=True)

        for geometry in shape_group.geometry:
            if geometry.geom_type == 'LineString':
                coords = [(lat, lon) for lon, lat in geometry.coords]
                f.PolyLine(
                    locations=coords,
                    color=color,
                    weight=3,
                    opacity=0.8,
                    tooltip=layer_name
                ).add_to(feature_group)
            else:
                print(f"[WARN] Geometry type not supported: {geometry.geom_type} (shape_id: {shape_id})")

        feature_group.add_to(base_map)
        route_count += 1

    f.LayerControl(collapsed=False).add_to(base_map)
    print(f"Map contains {route_count} transit routes.")
    return base_map


# --- MAIN ---
if __name__ == "__main__":
    engine = get_engine()
    hot_spot_routes_gdf = load_hot_spot_routes(engine).to_crs(epsg=4326)
    brooklyn_boundary_gdf = load_brooklyn_boundary(engine).to_crs(epsg=4326)

    route_map = create_routes_map(hot_spot_routes_gdf, brooklyn_boundary_gdf)
    route_map.save("outputs/hot_spot_routes_map.html")
    print("Mapa guardado como 'hot_spot_routes_map.html'")
