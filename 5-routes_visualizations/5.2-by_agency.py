from db_utils.db_connection import connect_to_database
import folium as f
import geopandas as gpd
from helpers.constants import agency_colors

def get_shapes_gdf(cur):
    sql = "SELECT * FROM route_shapes_view;"
    return gpd.GeoDataFrame.from_postgis(sql, cur.connection, geom_col='shape', crs='EPSG:4326')

def map_by_agency(gdf):
    m = f.Map(location=[40.7128, -74.0060], tiles='CartoDB positron', zoom_start=12)

    # Agrupar solo por agency_id (evita tuplas)
    for agency_id, group in gdf.groupby('agency_id'):
        color = agency_colors.get(agency_id, 'gray')
        fg = f.FeatureGroup(name=f"{agency_id}", show=True)

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
    m = map_by_agency(gdf)
    m.save("outputs/by_agency.html")
    print("Map saved to 'by_agency.html'")

if __name__ == "__main__":
    main()
