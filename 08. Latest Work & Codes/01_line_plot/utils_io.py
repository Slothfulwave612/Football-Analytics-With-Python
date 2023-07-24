"""
author : Anmol Durgapal (@slothfulwave612)

Python module containing utility functions for i/o operations.
"""

import pandas as pd
import calendar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

# so that browser wont open while scraping
chrome_options = Options()
chrome_options.add_argument("headless")


def get_data(link):
    """Function to scrape from understat given the link."""
    # ready the chrome-drivers
    driver = webdriver.Chrome(
        "/home/slothfulwave612/chromedriver_linux64/chromedriver",
        chrome_options=chrome_options
    )

    # give the link
    driver.get(link)

    # get the match data
    content = driver.execute_script("return shotsData;")

    # close the driver
    driver.close()

    return content


def get_date_dict(link_dict, season="2020"):
    """
    Function to get dictionary for 
    players listed inside link_dict.

    Parameters
    ----------
    link_dict : dict
        Containing player name as key and webpage link as value.
    season : str, defaults "2020"
        The season number.

    Returns
    -------
    dict : Containing key as player-name and value as 
           pandas.Series having dates when he scored.
    """
    # initialize empty dict
    date_dict = {}

    # traverse and make final series
    for key in tqdm(link_dict, desc=f"Scrapping Contents", total=len(link_dict)):
        # scrape and convert to dataframe
        df = pd.DataFrame(get_data(link_dict[key]))

        # fetch required dates
        date = df.loc[
            (df["season"] == season) &
            (df["result"] == "Goal")
        ].reset_index(drop=True)["date"].str[:10]

        # convert to datetime
        date = pd.to_datetime(
            date, format="%Y-%m-%d"
        )

        # assign the value
        date_dict[key] = date
    
    return date_dict


def get_month_dict(date_dict):
    """
    Function to get month dict.

    Parameters
    ----------
    date_dict : dict
        Containing key as player-name and value as 
        pandas.Series having dates when he scored.
    
    Returns
    -------
    dict : key --> month-number & value --> month-name.
    """
    # fetch the min-month
    min_month = min([
        value.min().month for value in date_dict.values()
    ])

    # fetch the max-month
    max_month = max([
        value.max().month for value in date_dict.values()
    ])

    # make month list
    month_list = list(range(min_month, 13)) + list(range(1, max_month + 1))

    # make month dict
    month_dict = dict(zip(
        (month for month in month_list),
        (
            calendar.month_name[month] if month >= min_month \
                else calendar.month_name[month] \
                    for month in month_list
        )
    ))

    return month_dict


def get_final_dataframe(date_dict, month_dict):
    """
    Function to get final dataframe containing
    player-names and goals they scored in each month.

    Parameters
    ----------
    date_dict : dict
        Containing key as player-name and value as 
        pandas.Series having dates when he scored.
    month_dict : dict
        key --> month-number & value --> month-name.
    
    Returns
    -------
    dict : Containing player-name and goals scored in each month.
    """
    # traverse the dict
    for count, key in enumerate(date_dict):
        # make dataframe
        temp_df = pd.DataFrame(
            date_dict[key]
        )

        # fetch months
        temp_df["month"] = temp_df["date"].dt.month

        # get number of goals scored in each month
        temp_df = temp_df.groupby(
            by="month", sort=False
        ).count()

        # change name of the column
        temp_df.columns = [key]

        # reset index
        temp_df = temp_df.reindex(month_dict.keys())

        # get cumulative sum
        temp_df[key] = temp_df[key].cumsum()

        if count == 0:
            df = temp_df.copy()
        else:
            df = df.join(temp_df, how="outer")
    
    # fill NaN values
    df.fillna(method='ffill', inplace=True)
    df.fillna(0, inplace=True)
        
    return df
