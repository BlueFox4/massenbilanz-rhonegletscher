import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_data(month, year):
    url = f"https://de.tutiempo.net/klima/{month}-{year}/ws-67200.html"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    list_header = []
    try:
        header = soup.find_all("table")[0].find("tr")
    except:
        print(f"Data not found for {month}-{year}")
        return

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # for getting the data 
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    # Storing the data into Pandas DataFrame
    dataFrame = pd.DataFrame(data = data, columns = list_header)
    
    # Converting Pandas DataFrame to CSV
    dataFrame.to_csv(f'massenbilanz-rhonegletscher/data/rhonegletscher_{year}_{month}.csv')

for year in range(1955, 2024):
    for month in range(1, 13):
        if month < 10:
            month = f"0{month}"
        get_data(month, year)