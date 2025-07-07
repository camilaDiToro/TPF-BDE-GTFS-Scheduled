import folium as f
import geopandas as gpd
from db_utils.db_connection import get_engine

def map_individual_lines():
    sql = 'SELECT * FROM shapes_aggregated;'
    try:
        engine = get_engine()
        shapes_gdf = gpd.read_postgis(sql, engine, geom_col='shape', crs='EPSG:4326')
        print(f"Loaded {len(shapes_gdf)} transit line records")
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

    # Crear el mapa centrado en Nueva York
    map_indiv_lines = f.Map(location=[40.7128, -74.0060], tiles='CartoDB positron',
                            zoom_start=13, control_scale=True)

    # Agrupar por shape_id y agregar las líneas al mapa
    route_count = 0
    for shape_id, shape_group in shapes_gdf.groupby('shape_id'):
        feature_group = f.FeatureGroup(name=f"Route {shape_id}", show=True)

        for geometry in shape_group.geometry:
            if geometry.geom_type == 'LineString':
                coords = [(lat, lon) for lon, lat in geometry.coords]
                f.PolyLine(locations=coords, color="blue", weight=2, opacity=0.8).add_to(feature_group)

        feature_group.add_to(map_indiv_lines)
        route_count += 1

    f.LayerControl(collapsed=False).add_to(map_indiv_lines)
    print(f"Created map with {route_count} transit routes")
    return map_indiv_lines


def main():
    """Función principal del script."""
    print("Starting Transit Lines Mapping Script...")
    print("=" * 50)

    individual_lines_map = map_individual_lines()
    if not individual_lines_map:
        return

    output_file = 'outputs/transit_lines_map.html'
    individual_lines_map.save(output_file)
    print(f"Map saved as '{output_file}'")

    print("=" * 50)
    print("SUCCESS! Your transit map has been created.")
    print(f"Open '{output_file}' in your web browser to view the interactive map.")


if __name__ == "__main__":
    main()