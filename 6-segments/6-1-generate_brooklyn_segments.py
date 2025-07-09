import gtfs_functions as gtfs
import os
from db_utils.db_connection import save_to_postgis

def load_gtfs_feed(file_path, start_date, end_date):
    feed = gtfs.Feed(file_path, start_date=start_date, end_date=end_date)
    return feed.segments

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    start_date = '2025-07-15'
    end_date = '2025-07-31'

    gtfs_path = os.path.join(base_dir, "../GTFS_SCHEDULED_ROOT_FOLDER/gtfs/gtfs_b.zip")
    segments_gdf = gtfs.Feed(gtfs_path, start_date=start_date, end_date=end_date).segments
    print(f"Saving {len(segments_gdf)} rows from gtfs_b.zip")
    save_to_postgis(
        segments_gdf,
        table_name="segments",
        schema="brooklyn",
        if_exists='replace'
    )
