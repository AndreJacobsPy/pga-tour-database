from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

import pandas as pd
from typing import List
from os import mkdir
from os.path import isdir

URL = "https://datagolf.com/historical-tournament-stats?event_id=26"
XPATH_HEAD = "/html/body/div[2]/div[2]/div[10]/div/div[2]"
FIRST = 0
LAST = 155

def open_website(url) -> Chrome:
    driver = Chrome()
    driver.get(url)

    return driver

def get_data(driver: Chrome, XPATH) -> WebElement:
    header = driver.find_element(by=By.XPATH, value=XPATH)
    return header

def select_tab(driver: Chrome, round: int) -> None:
    tab: WebElement = driver.find_element(by=By.XPATH, value='//*[@name="r{}"]'.format(round))
    tab.click()

def scrape(selecttab=0) -> pd.DataFrame:
    # set up dataset
    tournament_data = []

    # open webpage
    driver = open_website(URL)

    # select round to get data from
    if selecttab != 0:
        select_tab(driver, selecttab)

    # scraping
    header: str = get_data(driver, XPATH_HEAD).text
    tournament_data.append(header.lower().split('\n'))

    for i in range(FIRST, LAST + 1):
        xpath_row = '//*[@row_num="{}"]'.format(i)
        row: str = get_data(driver, xpath_row).text   
        tournament_data.append(row.lower().split('\n'))

    # closing the browser window
    driver.close()

    # convert to dataframe
    tournament_df = pd.DataFrame(data=tournament_data[1:], columns=tournament_data[0])

    return tournament_df

def main() -> None:
    # make folder to hold data
    if not isdir('data'):
        mkdir('data')

    # get data for whole tournament
    tournament_df: pd.DataFrame = scrape()
    tournament_df = tournament_df.rename(columns={'r4': 'r4-total'})
    tournament_df.to_csv('data/tournament_stats.csv', index=False)

    # get data for first round
    names = [                       # names for the csv files
        'first_round_stats.csv', 
        'second_round_stats.csv', 
        'third_round_stats.csv',
        'fourth_round_stats.csv'
    ]

    dataframes: List[pd.DataFrame] = [] # list to hold dataframes from loop
    for i in range(1, 5):
        dataframes.append(scrape(i))

    # loop to create csv files
    index = 0
    while index < 4:
        dataframes[index].to_csv(f'data/{names[index]}', index=False)
        index += 1

if __name__ == "__main__":
    main()  
