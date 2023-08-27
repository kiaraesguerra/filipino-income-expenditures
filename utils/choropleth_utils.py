import geopandas as gpd
import matplotlib.pyplot as plt


def get_string_inside_parenthesis(name):
    inside = name[name.find("(") + 1 : name.find(")")]
    inside = inside.split()
    return inside[0] if len(inside) == 1 else inside[1]


def make_map_text(name):
    text = name.split(" ")
    return text[1] if name.startswith("Region") else text[0]


def load_regions_geodataframe():
    regions_gdf = gpd.GeoDataFrame.from_file("data/ph-regions-2015.shp")
    regions_gdf.REGION = regions_gdf.REGION.apply(
        get_string_inside_parenthesis
    )  # Renaming the numbered regions to their numbers
    regions_gdf_clean = regions_gdf.drop(
        regions_gdf.index[-1]
    )  # Drop the last row (NIR)
    return regions_gdf_clean

def clean_region_names(data):
    data["Region"] = [
        entry.split()[0] for entry in data["Region"]
    ]  # Representing the regions with numbers
    data.loc[
        6, "Region"
    ] = "IV-A"  # Match the entry in regions_clean
    data.loc[
        7, "Region"
    ] = "IV-B"  # match the entry in regions_clean
    data.loc[
        2, "Region"
    ] = "XIII"  # match the entry in regions_clean
    return data



def regional_averages_name_clean(data, keys):
    regional_average_columns = data.groupby("Region")[keys].mean().reset_index()
    regional_average_columns["Region"] = [
        entry.split()[0] for entry in regional_average_columns["Region"]
    ]  # Representing the regions with numbers
    regional_average_columns.loc[
        6, "Region"
    ] = "IV-A"  # Match the entry in regions_clean
    regional_average_columns.loc[
        7, "Region"
    ] = "IV-B"  # match the entry in regions_clean
    regional_average_columns.loc[
        2, "Region"
    ] = "XIII"  # match the entry in regions_clean
    return regional_average_columns


def choropleth(merged_df, key):
    plt.style.use("ggplot")
    _, ax = plt.subplots(figsize=(10, 10))
    merged_df.plot(ax=ax, cmap="viridis", column=key, linewidth=1, legend=True)
    region_order = merged_df["Region"]
    for i, point in merged_df.iterrows():
        point_centroid = point.geometry.centroid
        reg_n = region_order[i]
        ax.text(s=reg_n, x=point_centroid.x, y=point_centroid.y, fontsize="large")

    ax.set_title("PH Administrative Regional Data", fontfamily="helvetica", fontsize=20)
    ax.set_axis_off()