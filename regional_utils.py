import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
from fuzzywuzzy import process


def bar_chart_regional_average(data, key: list):
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
    r_squared_text = f"r^2 = {1 - (residual_sum_of_squares / total_sum_of_squares):.2f}"
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
    # plt.text(0, 0, best_fit_line_text, horizontalalignment='center', verticalalignment='center', fontsize=12, color='red')

    # Calculate R-squared
    r_squared, r_squared_text = _r_squared(
        regional_averages_data["Total Household Income"], regional_averages_data[key]
    )
    # plt.text(0, 0, r_squared_text, horizontalalignment='center', verticalalignment='center', fontsize=12, color='red')

    # # Add region labels to the data points
    # for region, income, expenditure in zip(regional_averages.index, regional_averages['Total Household Income'], regional_averages[key]):
    #     plt.annotate(region, (income, expenditure), textcoords="offset points", xytext=(0,5), ha='center')



def get_string_inside_parenthesis(name):
    inside = name[name.find("(")+1:name.find(")")]
    inside = inside.split()
    return inside[0] if len(inside) == 1 else inside[1]

def make_map_text(name):
    text = name.split(' ')
    return text[1] if name.startswith('Region') else text[0]