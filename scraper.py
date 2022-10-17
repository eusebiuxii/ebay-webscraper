import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    url = f'https://www.ebay.co.uk/sch/i.html?_fsrp=1&_sacat=139971&_trkparms=pageci%3A7fb1a86e-4aec-11ed-9eb9-1a635f24d896%7Cparentrq%3Ad129ae221830a0d30a930a54ffeec5a0%7Ciid%3A1&{page}'
    #We need these details (headers/url) for our code to request the correct data from the webpage
    
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    #We use 'html.parser' to get the HTML data we need and store it in 'soup' variable

    return soup


def transform(soup):
    divs = soup.find_all('div', class_ = 's-item__wrapper clearfix')
    #We are now looking for specific divs, which in this case, are the wrapper of each and every item on the page
    
    
    for item in divs:
        #We loop through them, one by one, extracting the product information
        
            #Title
        
        substring1 = 'New listing'
        substring2 =' '
        tempOutString = ''
        title = ''
        
        tempString1 = item.find('div', class_ = 's-item__title').text.strip()
        #This is a div containing the name of the product posting. We strip it of white space
        tempString2 = tempString1.split(substring1)
        #As some product titles start with 'New listing' which we don't need so we strip it off
        for e in tempString2:
            tempOutString += e
        
        #We also split using the white space, as the titles are fairly long, however the information we need is in the first 5 - 10 words
        tempString3 = tempOutString.split(substring2)
        count = 0
        for i in tempString3:
            if count < 7:
                title += i + ' '
            count +=1
        
            #Subtitle
        subtitle = item.find('div', class_ = 's-item__subtitle').text.strip()
        #Same structure as for the title
        
            #Price
        price = item.find('div', class_ = 's-item__detail s-item__detail--primary').text.strip()
        #Same structure as for the title
        
            #List
        consoles = {
            'title': title,
            'subtitle': subtitle,
            'price': price
        }
        #We create a dictionary in order to store the data more efficiently
        game.append(consoles)
        #We then add this to the empty list 'game'
      
    return

#Main

game = []

for i in range(10):    
    print(f'Getting page, {i}')
    #We get each page one by one, printing as we go to know where we are (useful when extracting more than 6 pages worth of data)
    if i == 0:
        c = extract('')
        transform(c)
        #For the first page, the end of the URL doesn't change, therefore we do not add the page number 
    elif i != 0:
        c = extract(f'_pgn={i}')
        #We add the page number to the URL in this format (this format was derived from examining how the URL changes when going from page one to page two etc.)
        transform(c)

df = pd.DataFrame(game)
#We use a data frame to store the data we scraped
print(df)
#We print it to check the validity of the data
df.to_excel('gameConsoles.xlsx')
#We then transfer this data into an excel file to better visualise it