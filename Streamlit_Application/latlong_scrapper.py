import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import pickle

#First we have to create a url so that we can pass that url to browser and get the content of the page

#commonpart of url for any google search : "base url for google search"
base_url = 'https://www.google.com/search?q='

#Since we are going to send url to browser through a code we nead to set the header as follow so that browser will think it is geniune request
#and not the request from the bot
#Headers to simulate real browser visit
header = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def get_coordinates(sector):
    #search_term = f"sector {sector} in gurgaon longitude & latitude"
    search_term = f"{sector} in gurgaon longitude & latitude"
    #send the url to the browser using request.get
    response = requests.get(base_url + search_term, headers = header)

    # if we get ststus_code = 200 that indicates sucess if we get request code 404 that indicates failure
    if response.status_code == 200:
        #then extract the html content of that page using request.content
        soup = BeautifulSoup(response.content, 'html.parser')
        #find the respective div and class_ using inspect code on google page where required information is present
        coordinates_div = soup.find("div", class_ = "Z0LcW t2b5Cf")
        if coordinates_div :
            #extract the required info using .text
            return coordinates_div.text
    return None

with open("df.pkl", 'rb') as file:
    df_old = pickle.load(file)


list_sec_cord = []
for sector in list(sorted(np.unique(df_old['sector']))):
    coordinates = get_coordinates(sector)
    print(sector, coordinates)
    list_sec_cord.append([sector, coordinates])

df = pd.DataFrame(list_sec_cord, columns = ['sector', 'coordinates'])
df.to_csv("gurgaon_sectors_coordinates.csv", index=False)