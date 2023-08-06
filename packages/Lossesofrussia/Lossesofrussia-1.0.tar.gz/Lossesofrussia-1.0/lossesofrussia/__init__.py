import requests
from bs4 import BeautifulSoup

url = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

russian_items = bs.find('div', class_ = 'casualties').find_all('li')
personnel = russian_items[12].text
tanks = russian_items[0].text
bbm = russian_items[1].text
cannons = russian_items[2].text
mlrs = russian_items[3].text
anti_aircraft_warfare = russian_items[4].text
planes = russian_items[5].text
helicopters = russian_items[6].text
drones = russian_items[7].text
cruise_missiles = russian_items[8].text
warships = russian_items[9].text
cars = russian_items[10].text
special_equipment = russian_items[11].text


url = 'https://index.minfin.com.ua/en/russian-invading/casualties/'
response = requests.get(url)
bs = BeautifulSoup(response.text, 'html.parser')

russian_items_eng = bs.find('div', class_ = 'casualties').find_all('li')
personnel_eng = russian_items_eng[12].text
tanks_eng = russian_items_eng[0].text
bbm_eng = russian_items_eng[1].text
cannons_eng = russian_items_eng[2].text
mlrs_eng = russian_items_eng[3].text
anti_aircraft_warfare_eng = russian_items_eng[4].text
planes_eng = russian_items_eng[5].text
helicopters_eng = russian_items_eng[6].text
drones_eng = russian_items_eng[7].text
cruise_missiles_eng = russian_items_eng[8].text
warships_eng = russian_items_eng[9].text
cars_eng = russian_items_eng[10].text
special_equipment_eng = russian_items_eng[11].text


time = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
response = requests.get(time)
soup = BeautifulSoup(response.text, 'html.parser')

time2 = soup.find('span', class_ = 'black')
date = time2.text