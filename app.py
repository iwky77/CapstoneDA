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
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped table-hover table-hover-solid-row table-simple history-data'})
tr = table.find_all('tr')
td = table.find_all('td')
a = table.find_all('a')

#row_length = len(___)

temp = [] #initiating a list 

for i in range(0, len(tr)):
    
    row = table.find_all('tr')[i]
    if len(row) == 4:

        #getting 'date' data info:
        date = row.find_all('td')[0].text
        date = date.strip() #to remove excess white space

        #getting 'day' data info:
        day = row.find_all('td')[1].text
        day = day.strip() #to remove excess white space
   
        #getting 'rate value' data info:
        idr = row.find_all('td')[2].text
        idr = idr.strip() #to remove excess white space
    
        #getting 'additional info' data info:
        note = row.find_all('td')[3].text
        note = note.strip() #to remove excess white space
 
    temp.append((date,day,idr,note)) 

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','day','idr','note'))

#insert data wrangling here
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month_name()
df['idr'] = df['idr'].str.replace(" IDR","")
df['idr'] = df['idr'].str.replace(",","")
df['idr'] = df['idr'].astype('float64').round(2)
df = df.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'USD {df["idr"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
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