from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option(name="detach", value=True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://fantasy.premierleague.com/statistics")

cookie_button = driver.find_element(
    By.XPATH, value='//*[@id="onetrust-accept-btn-handler"]')
cookie_button.click()

view = Select(driver.find_element(By.ID, value='filter'))
view.select_by_index(3)
sorted_by = Select(driver.find_element(By.ID, value='sort'))
sorted_by.select_by_index(0)

page_source = driver.page_source

soup = BeautifulSoup(page_source, 'html.parser')

players = soup.find_all(class_="ElementInTable__Name-y9xi40-1 heNyFi")
teams = soup.find_all(class_="ElementInTable__Team-y9xi40-3 hosEuf")
costs = soup.select(
    '.ElementTable__ElementRow-sc-1v08od9-3.kGMjuJ td:nth-of-type(3)')
total_points = soup.select(
    '.ElementTable__ElementRow-sc-1v08od9-3.kGMjuJ td:nth-of-type(6)')

data = []

for player, team, cost, total_point in zip(players, teams, costs, total_points):
    row = {
        'player': player.text,
        'team': team.text,
        'cost': cost.text,
        'total point': total_point.text,
        'point per cost': float(total_point.text)/float(cost.text)
    }
    data.append(row)

df = pd.DataFrame(data)
driver.quit()
