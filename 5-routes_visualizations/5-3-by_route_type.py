from db_utils.db_connection import connect_to_database
import folium as f
import geopandas as gpd
from helpers.constants import agency_colors, route_type_colors, route_type_name

def get_shapes_gdf(cur):
    sql = "SELECT * FROM route_shapes_view;"
    return gpd.GeoDataFrame.from_postgis(sql, cur.connection, geom_col='shape', crs='EPSG:4326')

def map_by_route_type(gdf):
    m = f.Map(location=[40.7128, -74.0060], tiles='CartoDB positron', zoom_start=12)
    for route_type, group in gdf.groupby('route_type'):
        color = route_type_colors.get(route_type, 'black')
        name = route_type_name.get(route_type, '')
        fg = f.FeatureGroup(name=f"{route_type} - {name}", show=True)
        for geom in group.geometry:
            if geom.geom_type == 'LineString':
                coords = [(lat, lon) for lon, lat in geom.coords]
                f.PolyLine(locations=coords, color=color, weight=2, opacity=0.8).add_to(fg)
        fg.add_to(m)
    f.LayerControl(collapsed=False).add_to(m)
    return m

def main():
    cur = connect_to_database()
    if not cur:
        return
    gdf = get_shapes_gdf(cur)
    if gdf.empty:
        print("No shapes loaded.")
        return
    m = map_by_route_type(gdf)
    m.save("outputs/by_type.html")
    print("Map saved to 'by_type.html'")

if __name__ == "__main__":
    main()
