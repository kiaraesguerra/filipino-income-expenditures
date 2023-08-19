import numpy as np
import pandas as pd


def get_best_fit_line(x, y) -> tuple:
    """Calculate the best fit line for the given data."""
    coefficients = np.polyfit(x, y, 1)
    slope, intercept = coefficients
    equation_text = f"y = {slope:.2f}x + {intercept:.2f}"
    return slope * x + intercept, equation_text


def get_r_squared(x, y) -> tuple:
    """Calculate the R-squared value for the given data."""
    y_mean = np.mean(y)
    total_sum_of_squares = np.sum((y - y_mean) ** 2)
    residual_sum_of_squares = np.sum((y - get_best_fit_line(x, y)[0]) ** 2)
    r_squared_text = f"R^2 = {1 - (residual_sum_of_squares / total_sum_of_squares):.2f}"
    return 1 - (residual_sum_of_squares / total_sum_of_squares), r_squared_text


def get_region_with_min_max_value(data, key):
    """Return the region with the highest / lowest average value for the given data column."""
    regional_averages_data = data.groupby("Region")[key].mean()
    return regional_averages_data.idxmax(), regional_averages_data.idxmin()


def create_dataframe_min_max(data, keys):
    """Return a dataframe with the highest / lowest average value for the given data column."""
    max_min = {}
    for key in keys:
        max_val, min_val = get_region_with_min_max_value(data, key)
        max_min.update({key: [max_val, min_val]})

    return pd.DataFrame(max_min)


def get_income_expenditure_r_squared(data, key):
    regional_income_data = data.groupby("Region")["Total Household Income"].mean()
    """Return the region with the highest / lowest average value for the given data column."""
    regional_averages_data = data.groupby("Region")[key].mean()
    r_squared = get_r_squared(regional_income_data, regional_averages_data)

    return r_squared


def create_dataframe_r_squared(data, keys):
    """Return a dataframe with the highest / lowest average value for the given data column."""
    r_ = {}
    for key in keys:
        r2_val, _ = get_income_expenditure_r_squared(data, key)
        r_val = np.sqrt(r2_val)
        r_.update({key: [r2_val, r_val]})

    return pd.DataFrame(r_)


# def map_names_clean():
#     psgg_code = pd.read_csv('map/psgg_codes.csv', dtype=object)
#     map_names = psgg_code.loc[:, ['psgg_code', 'region']]
#     map_names['region'] = map_names['region'].apply(lambda x: make_map_text(x))
#     map_names.set_index('psgg_code', inplace=True, drop=True)

#     return map_names
