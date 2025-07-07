import gtfs_functions as gtfs
import os

from db_utils.db_connection import save_to_postgis

def load_gtfs_feed(file_path, start_date, end_date):
    feed = gtfs.Feed(file_path, start_date=start_date, end_date=end_date)
    return feed.segments

if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    start_date = '2025-07-20'
    end_date = '2025-07-22'

    gtfs_files = [
        "gtfs_b.zip",
        "gtfs_busco.zip",
        "gtfs_q.zip",
    ]

    schema = [
        "brooklyn",
        "busco",
        "queens",
    ]

    for i, filename in enumerate(gtfs_files):
        gtfs_path = os.path.join(base_dir, "../GTFS_SCHEDULED_ROOT_FOLDER/gtfs", filename)
        segments_gdf = gtfs.Feed(gtfs_path, start_date=start_date, end_date=end_date).segments
        print(f"Saving {len(segments_gdf)} rows from {filename}")
        save_to_postgis(
            segments_gdf,
            table_name="speed_segments",
            schema=schema[i],
            if_exists='replace'
        )
