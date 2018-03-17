from bs4 import BeautifulSoup
import urllib
import pandas as pd
import re

chi = 'https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_Chicago'
nyc = 'https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_New_York_City'
dc = 'https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_Washington,_D.C.'
sfb = 'https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_the_San_Francisco_Bay_Area'

def getTable(url):
    f = urllib.urlopen(url).read()
    soup = BeautifulSoup(f)
    return soup

def parseTable(soup):
    headers = [x.text.encode('utf8') for x in soup.table.find_all('th')]
    rows = soup.table.find_all('tr')[1:]
    L = []
    L.append(headers)
    j = len(headers)
    for row in rows:
        r = parseRow(row,j)
        L.append(r)
    return L

def parseRow(r,j):
    R = []
    row = r.find_all('td')
    for i in range(0,j):
        try:
            cell = row[i]
            if cell.img is not None:
                stars = str(cell.img['alt'])
                try:
                    starnum = re.match('([1-3])',stars).group(0)
                except AttributeError:
                    starnum = '0'
                R.append(starnum)
            else:
                R.append(str(cell.text.encode('utf8')))
        except IndexError:
            R.append('Closed')
    return R

def parseCity(url,outputFilename):
    f = urllib.urlopen(url)
    soup = BeautifulSoup(f)
    L = parseTable(soup)
    headers = L.pop(0)
    df = pd.DataFrame(L,columns=headers)
    df.to_csv(outputFilename)

urls = [chi,nyc,dc,sfb]
names = ['chicago.csv','newyork.csv','dc.csv','sfbayarea.csv']
Z = zip(urls,names)
for each in Z:
    parseCity(each[0],each[1])