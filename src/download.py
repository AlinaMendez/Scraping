import requests 
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt

url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text
#print(html_data)
result = BeautifulSoup(html_data,"html.parser")
#print(result)
tables = result.find_all("table")
#print(tables)

for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        my_index = index
#print(my_index)

df = pd.DataFrame(columns=['Date', 'Revenue'])

for row in tables[my_index].tbody.find_all('tr'):
    col = row.find_all('td')
    if (col != []):
        Fecha = col[0].text
        Ingreso = col[1].text.replace("$", "").replace(",", "")
        df = df.append({"Date":Fecha, "Revenue":Ingreso}, ignore_index=True)

df = df[df['Revenue'] != ""] # elimino los datos nulos
print(df)
print(type(df))

records = df.to_records(index=False)
result = list(records)
#print(result)

connection = sqlite3.connect('Tesla.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS revenue
             (Date, Revenue)''')

cursor.executemany('INSERT INTO revenue VALUES (?,?)', result)
connection.commit()
for x in cursor.execute('SELECT * FROM revenue'):
    print(x)

df['Date'] = pd.to_datetime(df['Date'])
df['Revenue'] = df['Revenue'].astype('int64')
plt.figure()
plt.scatter(x=df['Date'], y=df['Revenue'])
plt.title("Tesla Quarterly Revenue")
plt.ylabel("Revenue (Millions of US $)")
plt.savefig("Revenue.jpg")

