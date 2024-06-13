import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os

def scrapper():
    sources = ['https://www.dawn.com/', 'https://www.bbc.com/']
    all_data = []
    for source in sources:
        response = requests.get(source)
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        data = [(tag.name, tag.get_text(strip=True)) for tag in tags]
        all_data.extend(data)
    return all_data

def data_transformation(extracted_data):
    df = pd.DataFrame(extracted_data, columns=['Tag', 'Content'])
    df['Content'] = df['Content'].str.replace(r'\n|\r', ' ', regex=True).str.strip()
    df.to_csv('transformed_data.csv', index=False)

def store_data():
    pass

if __name__ == "__main__":
    extracted_data = scrapper()
    data_transformation(extracted_data)
    store_data()
