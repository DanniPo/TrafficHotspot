import matplotlib.colors as colors
from matplotlib import colormaps
import pandas as pd
import geopandas as gpd
import folium
import hdbscan

CSV_PATH = r"C:\Users\HP\Downloads\Traffic_Crashes_-_Crashes_20250420.csv"
OUT_PATH = "clusters_map.html"


def plot_clusters_folium(dataframe):
    gdf = gpd.GeoDataFrame(
        dataframe,
        geometry=gpd.points_from_xy(dataframe["LONGITUDE"], dataframe["LATITUDE"]),
        crs="EPSG:4326",
    )

    center = [gdf["LATITUDE"].mean(), gdf["LONGITUDE"].mean()]
    fmap = folium.Map(location=center, zoom_start=11, tiles="CartoDB Positron")

    unique_clusters = sorted(gdf[gdf["Cluster"] != -1]["Cluster"].unique())
    n_colors = max(len(unique_clusters), 1)
    cmap = colormaps.get_cmap("tab20").resampled(n_colors)

    cluster_colors = {
        cluster: colors.to_hex(cmap(i)) for i, cluster in enumerate(unique_clusters)
    }

    for _, row in gdf.iterrows():
        color = "lightgray" if row["Cluster"] == -1 else cluster_colors[row["Cluster"]]
        folium.CircleMarker(
            location=[row["LATITUDE"], row["LONGITUDE"]],
            radius=2,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            weight=0,
            popup=f"Cluster: {row['Cluster']}",
        ).add_to(fmap)

    non_noise_items = "".join(
        (
            "<div style='margin:2px 0;'>"
            f"<span style='display:inline-block;width:10px;height:10px;"
            f"background:{cluster_colors[cluster]};margin-right:6px;'></span>"
            f"Cluster {cluster}</div>"
        )
        for cluster in unique_clusters
    )
    if not non_noise_items:
        non_noise_items = "<div style='color:#666;'>No non-noise clusters</div>"

    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 9999;
        background: white;
        border: 2px solid #999;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 12px;
        line-height: 1.25;
        max-height: 180px;
        overflow-y: auto;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
    ">
        <div style="font-weight: 700; margin-bottom: 6px;">Cluster Legend</div>
        <div style='margin:2px 0;'>
            <span style='display:inline-block;width:10px;height:10px;background:lightgray;margin-right:6px;'></span>
            Noise (-1)
        </div>
        <div style="font-weight: 600; margin: 6px 0 4px;">Non-noise clusters</div>
        {non_noise_items}
    </div>
    """
    fmap.get_root().html.add_child(folium.Element(legend_html))

    return fmap


def main():
    df = pd.read_csv(CSV_PATH)
    df["CRASH_DATE"] = pd.to_datetime(df["CRASH_DATE"])
    df = df[df["CRASH_DATE"].dt.year >= 2024]
    df = df.dropna(subset=["LATITUDE", "LONGITUDE"])
    df = df[df["LATITUDE"] != 0]
    df = df[df["LONGITUDE"] != 0]

    coords = (
        df[["LATITUDE", "LONGITUDE"]]
        .apply(lambda s: s.astype(str).str.replace(",", "", regex=False))
        .astype(float)
    )

    hdb = hdbscan.HDBSCAN(min_samples=None, min_cluster_size=3, metric="euclidean")
    coords_scaled = coords.copy()
    coords_scaled["LATITUDE"] = 2 * coords_scaled["LATITUDE"]
    coords["Cluster"] = hdb.fit_predict(coords_scaled)

    fmap = plot_clusters_folium(coords)
    fmap.save(OUT_PATH)
    print(f"Saved {OUT_PATH}")


if __name__ == "__main__":
    main()
