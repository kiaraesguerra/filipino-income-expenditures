import re
import numpy as np


def get_expenditures_data(data):
    expenditures_data = data.filter(
        regex=re.compile(r"expenditure", re.IGNORECASE)
    ).columns.tolist()
    expenditures_data.append("Crop Farming and Gardening expenses")
    return expenditures_data


def get_income_data(data):
    income_data = data.filter(
        regex=re.compile(r"income", re.IGNORECASE)
    ).columns.tolist()
    return income_data


def get_householdhead_data(data):
    householdhead_data = data.filter(
        regex=re.compile(r"household head", re.IGNORECASE)
    ).columns.tolist()
    return householdhead_data


def get_appliances_data(data):
    number_data = data.filter(
        regex=re.compile(r"number", re.IGNORECASE)
    ).columns.tolist()
    number_data.remove("Total Number of Family members")
    number_data.remove("Total number of family members employed")
    number_data.remove("Number of bedrooms")
    return number_data


def get_property_information(data):
    house_data = data.filter(regex=re.compile(r"type", re.IGNORECASE)).columns.tolist()
    house_data_additional = [
        "House Floor Area",
        "Tenure Status",
        "Toilet Facilities",
        "Electricity",
        "Main Source of Water Supply",
        "House Age",
        "Imputed House Rental Value",
        "Number of bedrooms",
        "Agricultural Household indicator",
    ]
    house_data.remove(
        "Type of Household"
    )  # This will be included in the family composition data
    house_data.extend(house_data_additional)
    return house_data


# Data regarding family composition
def get_family_composition(data):
    family_members_data = data.filter(
        regex=re.compile(r"members", re.IGNORECASE)
    ).columns.tolist()
    family_members_data.append("Type of Household")
    return family_members_data


def aggregate_householdhead_education(data):
    replacement_dict = {
        ".*Programs$": "Degree",
        "^Grade.*|Elementary Graduate": "Elementary",
        ".*College$": "College Undergrad",
        ".*High School$|High School Graduate": "High School",
        "^Other Programs.*|.*Post Secondary$": "Post Secondary",
        "No Grade Completed|Preschool$": "Pre Elem",
    }

    # Perform the replacements using regex
    data["Household Head Highest Grade Completed"] = data[
        "Household Head Highest Grade Completed"
    ].replace(replacement_dict, regex=True)
    data["Household Head Highest Grade Completed"].unique()

    return data


def remove_income_outlier(data):
    z_scores = np.abs(
        (data["Total Household Income"] - data["Total Household Income"].mean())
        / data["Total Household Income"].std()
    )
    threshold = 3
    outlier_indices = np.where(z_scores > threshold)[0]
    return data.drop(outlier_indices)




# # Checking if all of the columns have been categorized
# collection = expenditures_data +  income_data + number_data +  householdhead_data + family_members_data +  house_data
# missing = [element for element in data.columns if element not in collection]
# print(missing)
