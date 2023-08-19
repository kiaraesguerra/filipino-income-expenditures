
import matplotlib.pyplot as plt


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
    regional_average_column = (
        data.groupby("Region")[key].value_counts().unstack().reset_index()
    )
    ax = regional_average_column.plot(kind="bar", stacked=True, figsize=(10, 6))
    plt.title(key)
    plt.legend()
    ax.set_xticklabels(
        [entry.split()[0] for entry in regional_average_column["Region"]],
        rotation=0,
        ha="right",
    )
    plt.tick_params(size=16)
    plt.xlabel("Region", size=16)
    plt.ylabel("Number", size=16)
    fig = plt.gcf()
    fig.set_size_inches(20, 10)
    ax.grid(False)
    plt.show()
