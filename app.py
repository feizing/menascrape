import csv
import requests
from bs4 import BeautifulSoup as bsoup

page = "" # Page with our event listings
page = requests.get(page)
soup = bsoup(page.content,'lxml')

entries= []

for item in soup.find_all('div', class_='c-event-card c-event-card--listing c-col'):
    entry = {}

    title_element = item.find('h3', class_='c-event-card__title')
    entry['title'] = title_element.text.strip()

    anchor_element = title_element.find('a')
    entry['pagelink'] = anchor_element['href']

    buy_elements = item.find_all('div', class_='c-event-instance')
    buy_element_index = 1
    for buy_element in buy_elements:
        anchor_elem = buy_element.find('a', class_='c-event-instance__btn')
        entry[f'buylink{buy_element_index}_url'] = anchor_elem['href']
        date_elem = buy_element.find('div', class_='c-event-instance__date')
        time_elem = buy_element.find('div', class_='c-event-instance__time')
        entry[f'buylink{buy_element_index}_date'] = date_elem.text.strip() + ", " + time_elem.text.strip()
        buy_element_index += 1

    entries.append(entry)

with open('output.csv', mode='w') as sheet_file:
    fieldnames = ['title', 'pagelink','buylink1_date', 'buylink1_url', 'buylink2_date', 'buylink2_url']
    sheet_writer = csv.DictWriter(sheet_file, fieldnames=fieldnames)
    sheet_writer.writeheader()
    for entry in entries:
        sheet_writer.writerow(entry)

for entry in entries:
    print(entry)
