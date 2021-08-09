import concurrent.futures
from multiprocessing.dummy import freeze_support
from LegitimateTest import generate_data_set
import pandas as pd
from openpyxl import load_workbook
from multiprocessing import Pool

"""data = pd.read_csv("verified_online.csv")
data_frame = pd.DataFrame(data)
wb = load_workbook("New_list.xlsx")
ws = wb.worksheets[0]

url_list = []


for url in data_frame.iterrows():
    url_list.append(url[1][0])


for url2 in url_list:
    ws.append(generate_data_set(url2))
    wb.save("New_list.xlsx")"""



data = pd.read_csv("dataset.csv")
data_frame = pd.DataFrame(data)
data_frame.replace(9, -1, inplace= True)
"""for row in data_frame.iterrows():
    for index in range(30):
        print(row[1][index])"""

data_frame.to_csv("new.csv")

