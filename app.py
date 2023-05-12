from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
row = table.find_all('a', attrs={'class':'n'})
row_kurs=table.find_all('span', attrs={'class':'nowrap'})

row_length = len(row)
row_length_kurs = len(row_kurs)

Date = [] #initiating a list 
USDtoIDR = []

for i in range(0, row_length):
#insert the scrapping process here
    date = table.find_all('a',attrs={'class':'n'})[i].text
    
    Date.append((date))

for i in range(1,row_length_kurs,4):
    kurs_Rp=table.find_all('span',attrs={'class':'nowrap'})[i].text
    
    USDtoIDR.append((kurs_Rp))

Exchange = list(zip(Date, USDtoIDR))

Exchange=Exchange[::-1]

#change into dataframe
df = pd.DataFrame(Exchange, columns=['Date','USDtoIDR'])

#insert data wrangling here
df['USDtoIDR'] = df['USDtoIDR'].str.replace("Rp","")
df['USDtoIDR'] = df['USDtoIDR'].str.replace(",","")
df['USDtoIDR'] = df['USDtoIDR'].astype('float64')
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["USDtoIDR"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(x='Date', y='USDtoIDR',figsize = (20,9)) 
	ax.set_xlabel('Date')
	ax.set_ylabel('Exchange Rate (IDR/USD)')
	ax.set_title('USD to IDR Exchange Rate 5-Year History')

	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)