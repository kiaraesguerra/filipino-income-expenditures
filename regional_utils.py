import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
from fuzzywuzzy import process
from adjustText import adjust_text


def bar_chart_regional_average(data, key: str):
    """
    Plot a bar chart showing the regional average for the specified data column.

    Parameters:
        data (DataFrame): The input DataFrame containing the data and 'Region' column.
        value_column (str): The column name for which the regional average needs to be calculated.
    """
    # Create a new dataframe with the average values for each region
    regional_average_column = data.groupby("Region")[key].mean().reset_index()

    # Determine the indices of the highest and lowest values
    highest_idx = regional_average_column[key].idxmax()
    lowest_idx = regional_average_column[key].idxmin()

    # Create a list to hold bar colors
    colors = ["blue"] * len(regional_average_column[key])
    colors[highest_idx] = "green"
    colors[lowest_idx] = "red"

    # Plot the bar chart
    plt.figure(figsize=(20, 10))
    plt.bar(
        [entry.split()[0] for entry in regional_average_column["Region"]],
        regional_average_column[key],
        color=colors,
        alpha=0.5,
    )
    plt.tick_params(size=16)
    plt.xlabel("Region", size=16)
    plt.ylabel("Average " + key)
    plt.show()
    
def stacked_bar(data, key):
    regional_average_column = data.groupby('Region')[key].value_counts().unstack().reset_index()
    ax = regional_average_column.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title(key)
    plt.legend()
    ax.set_xticklabels([entry.split()[0] for entry in regional_average_column["Region"]],  rotation = 0, ha='right')
    plt.tick_params(size=16)
    plt.xlabel("Region", size=16)
    plt.ylabel('Number', size=16)
    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    ax.grid(False)
    plt.show()


def region_with_min_max_value(data, key):
    """Return the region with the highest / lowest average value for the given data column."""
    regional_averages_data = data.groupby("Region").mean()
    return regional_averages_data[key].idxmax(), regional_averages_data[key].idxmin()


def create_dataframe_min_max(data, keys):
    """Return a dataframe with the highest / lowest average value for the given data column."""
    max_min = {}
    for key in keys:
        max_val, min_val = region_with_min_max_value(data, key)
        max_min.update({key: [max_val, min_val]})

    return pd.DataFrame(max_min)


def _best_fit_line(x, y) -> tuple:
    """Calculate the best fit line for the given data."""
    coefficients = np.polyfit(x, y, 1)
    slope, intercept = coefficients
    equation_text = f"y = {slope:.2f}x + {intercept:.2f}"
    return slope * x + intercept, equation_text


def _r_squared(x, y) -> tuple:
    """Calculate the R-squared value for the given data."""
    y_mean = np.mean(y)
    total_sum_of_squares = np.sum((y - y_mean) ** 2)
    residual_sum_of_squares = np.sum((y - _best_fit_line(x, y)[0]) ** 2)
    r_squared_text = f"R^2 = {1 - (residual_sum_of_squares / total_sum_of_squares):.2f}"
    return 1 - (residual_sum_of_squares / total_sum_of_squares), r_squared_text


def regional_average_dependence(data, key):
    """Plot a scatter plot showing the relationship between the average total household income and the specified data column."""
    regional_averages_data = data.groupby("Region").mean()
    plt.figure(figsize=(20, 10))
    plt.scatter(
        regional_averages_data["Total Household Income"],
        regional_averages_data[key],
        s=100,
        c="blue",
        alpha=0.7,
    )
    plt.tick_params(axis="both", which="major", labelsize=16)
    plt.xlabel("Average Total Household Income", size=16)
    plt.ylabel("Average " + key, size=16)

    # Calculate best fit line
    best_fit_line, best_fit_line_text = _best_fit_line(
        regional_averages_data["Total Household Income"], regional_averages_data[key]
    )
    plt.plot(
        regional_averages_data["Total Household Income"],
        best_fit_line,
        color="red",
        label="Best Fit Line",
    )

    plt.annotate(
        best_fit_line_text,
        xy=(0.5, 0.45),
        fontsize=12,
        color="red",
        xycoords="axes fraction",
    )

    # Calculate R-squared
    r_squared, r_squared_text = _r_squared(
        regional_averages_data["Total Household Income"], regional_averages_data[key]
    )

    plt.annotate(
        r_squared_text,
        xy=(0.5, 0.4),
        fontsize=12,
        color="red",
        xycoords="axes fraction",
    )

    texts = []
    # Add region labels to the data points
    for region, income, expenditure in zip(
        regional_averages_data.index,
        regional_averages_data["Total Household Income"],
        regional_averages_data[key],
    ):
        texts.append(
            plt.annotate(
                region.split()[0],
                (income, expenditure),
                textcoords="offset points",
                xytext=(0, 5),
                ha="center",
                fontsize=12,
            )
        )

    adjust_text(texts, only_move={"points": "y", "texts": "y"})

    plt.show()


def income_expenditure_r_squared(data, key):
    """Return the region with the highest / lowest average value for the given data column."""
    regional_averages_data = data.groupby("Region").mean()
    r_squared =_r_squared(regional_averages_data['Total Household Income'], regional_averages_data[key])
    
    return r_squared

def create_dataframe_r_squared(data, keys):
    """Return a dataframe with the highest / lowest average value for the given data column."""
    r_squared = {}
    for key in keys:
        r_val, _ = income_expenditure_r_squared(data, key)
        r_squared.update({key: [r_val]})

    return pd.DataFrame(r_squared)


def get_string_inside_parenthesis(name):
    inside = name[name.find("(") + 1 : name.find(")")]
    inside = inside.split()
    return inside[0] if len(inside) == 1 else inside[1]


def make_map_text(name):
    text = name.split(" ")
    return text[1] if name.startswith("Region") else text[0]


def load_regions_geodataframe():
    regions_gdf = gpd.GeoDataFrame.from_file("map/ph-regions-2015.shp")
    regions_gdf.REGION = regions_gdf.REGION.apply(
        get_string_inside_parenthesis
    )  # Renaming the numbered regions to their numbers
    regions_gdf_clean = regions_gdf.drop(
        regions_gdf.index[-1]
    )  # Drop the last row (NIR)
    return regions_gdf_clean



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



def householdhead_education_aggregate(data):
    replacement_dict = {
        '.*Programs$': 'Degree',
        '^Grade.*|Elementary Graduate': 'Elementary',
        '.*College$': 'College Undergrad',
        '.*High School$|High School Graduate': 'High School',
        '^Other Programs.*|.*Post Secondary$': 'Post Secondary',
        'No Grade Completed|Preschool$': 'Pre Elem',
    }

    # Perform the replacements using regex
    data['Household Head Highest Grade Completed'] = data['Household Head Highest Grade Completed'].replace(replacement_dict, regex=True)
    data['Household Head Highest Grade Completed'].unique()
    
    return data

# def map_names_clean():
#     psgg_code = pd.read_csv('map/psgg_codes.csv', dtype=object)
#     map_names = psgg_code.loc[:, ['psgg_code', 'region']]
#     map_names['region'] = map_names['region'].apply(lambda x: make_map_text(x))
#     map_names.set_index('psgg_code', inplace=True, drop=True)

#     return map_names
