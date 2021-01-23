from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import webbrowser, zlib, time

# Web scraping function
def scrapeSite():
    my_url = 'https://www.rivcoph.org/COVID-19-Vaccine' # web URL
    uClient = uReq(my_url) # open URL
    page_html = zlib.decompress(uClient.read(), 16+zlib.MAX_WBITS) # decompress gzip
    uClient.close() # close URL
    page_soup = soup(page_html, 'html.parser') # parse URL data

    tables = page_soup.find(id='dnn_ctr2947_HtmlModule_lblContent') # find table with vaccination links

    links = [] # empty list for urls
    for link in tables.find_all('a'): # find anchors
        links.append(link.get('href')) # append urls to list

    b = webbrowser.get('chrome') # chrome is selected browser
    for url in links: # iterate through list of urls
        if 'Full.png' in url: # if href contains "full" image directory
            pass # skip
        else:
            b.open(url) # open the url in chrome
            print(url) # print the url
    print('\n\nDONE!\n') #complete message

# Run script to completion
def main():
    while True:
        try: # try running the script
            scrapeSite()
            break # break once scrapeSite() function completely executes
        except: # Any error
            time.sleep(1) # wait 1 second
            pass # skip / try again
        else: 
            break


# Run script
main()