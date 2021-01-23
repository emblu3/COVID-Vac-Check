from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import webbrowser, zlib

def scrapeSite():
    # Web scraping function
    my_url = 'https://www.rivcoph.org/COVID-19-Vaccine' #web URL
    uClient = uReq(my_url) #open URL
    page_html = zlib.decompress(uClient.read(), 16+zlib.MAX_WBITS)
    uClient.close() #close URL
    page_soup = soup(page_html, 'html.parser') #parse URL data

    tables = page_soup.find(id='dnn_ctr2947_HtmlModule_lblContent')

    links = []
    for link in tables.find_all('a'):
        links.append(link.get('href'))

    b = webbrowser.get('chrome')
    for url in links:
        if 'Full.png' in url:
            pass
        else:
            b.open(url)
            print(url)
    print('\n\nDONE!\n')

def forever():
    while True:
        try:
            scrapeSite()
            break
        except:
            pass
        else:
            break

forever()



