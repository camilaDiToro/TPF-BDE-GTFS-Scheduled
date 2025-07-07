import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from db_utils.db_connection import get_engine

# Query data and generate histograms
def plot_speed_histograms():
    engine = get_engine()

    query = f"""
        SELECT
        CASE EXTRACT(DOW FROM t_arrival AT TIME ZONE 'America/New_York')
            WHEN 0 THEN 'Sunday'
            WHEN 1 THEN 'Monday'
            ELSE 'unknown'
        END AS weekday,
        EXTRACT(HOUR FROM t_arrival AT TIME ZONE 'America/New_York') AS hour,
        COUNT(*) AS num_segments,
        AVG(speed) AS avg_speed
        FROM segments_with_speed
        WHERE t_arrival >= '2025-07-20 00:00:00 America/New_York'
          AND t_arrival <  '2025-07-22 00:00:00 America/New_York'
        GROUP BY weekday, hour
        ORDER BY weekday, hour;
    """

    df = pd.read_sql(query, engine)

    sns.set(style="whitegrid")

    full_hours = pd.Series(range(24), name="hour")  # 0 to 23

    for day in df['weekday'].unique():
        day_df = df[df['weekday'] == day].copy()
        day_df['hour'] = day_df['hour'].astype(int)

        # Reindex to ensure all hours 0–23 are included
        day_df = full_hours.to_frame().merge(day_df, on="hour", how="left")
        day_df['weekday'] = day  # fill missing weekday values
        day_df['num_segments'] = day_df['num_segments'].fillna(0).astype(int)
        day_df['avg_speed'] = day_df['avg_speed'].fillna(0)  # or np.nan if you prefer empty bars

        total_segments = day_df['num_segments'].sum()

        plt.figure(figsize=(10, 6))
        sns.barplot(x='hour', y='avg_speed', data=day_df, color='blue')
        plt.title(f"{day} - Average Speed by Hour\n{int(total_segments)} segments considered")
        plt.xlabel("Hour of Day")
        plt.ylabel("Average Speed (km/h)")
        plt.xticks(range(0, 24))
        plt.tight_layout()
        plt.savefig(f"outputs/histograms/speed_histogram_{day.lower()}.png")
        plt.close()
        print(f"Saved: speed_histogram_{day.lower()}.png")

if __name__ == "__main__":
    plot_speed_histograms()
