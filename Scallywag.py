from bs4 import BeautifulSoup
import urllib3
import requests
import argparse
from requests.exceptions import SSLError, ConnectionError

def soupify(url):
    page = http.request('GET', url)
    return BeautifulSoup(page.data.decode('utf-8'), "html.parser")

def get_table_data(soup):
    all_table_rows = soup.findAll('tr')
    all_data = []
    for row in all_table_rows:
        try:
            all_data.append(row.findAll('td'))            
        except IndexError:
            pass
    return all_data

def get_magnet(soup):
    download_data = soup.find_all("div", class_="download")[0].find_all('a')[0].get('href')
    return download_data

def get_args():
    parser = argparse.ArgumentParser(description='Get latest movie torrents')
    parser.add_argument('-k', '--keyword', help='keyword to search for movies', required=False, default='')
    parser.add_argument('-p', '--pages', help='Enter number of pages to view', required=False, default=2)
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    keyword = args.keyword.lower()
    pages = int(args.pages)

    http = urllib3.PoolManager()
    proxy_soup = soupify("https://piratebay-proxylist.net/")
    
    proxy_data = get_table_data(proxy_soup)
    proxy_data = [data.get('data-href') for sub_data in proxy_data for data in sub_data if data.get('data-href') != None]
    
    for site in proxy_data:
        print('trying: '+ str(site))
        try:
            r = requests.get(site)
        except (SSLError, ConnectionError):    
            print('/t failed: ' + str(site))
            print('Try again. If that fails, try using a VPN (or maybe go the theatre next time)')        
            pass    
        else:
            if r.status_code == 200:
                print('using site: ' + str(site))
                for i in range(0, pages):
                    pirate_soup = soupify(site+'/browse/207/' + str(i) + '/7')
                    pirate_data = get_table_data(pirate_soup)
                    pirate_data = [data.findAll('a') for sub_data in pirate_data for data in sub_data if data.findAll('a') != None]

                    for sub_data in pirate_data:
                        for data in sub_data:
                            if data.get('class'):
                                if data.get('class')[0] == 'detLink':
                                    title = data.string.replace('.',' ')
                                    if keyword in title.lower():
                                        print(title)
                                        magnet_soup = soupify(site + data.get('href'))
                                        magnet = get_magnet(magnet_soup)
                                        print(str(magnet) + '\n')             
                break




    
    


