from bs4 import BeautifulSoup
import requests
import argparse
import json

base_url = "https://finviz.com/"

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--strings_scrape',
                    help="Provide strings to scrape the data")
args = parser.parse_args()
search_text = args.strings_scrape
cookies = {
    'screenerUrl': 'screener.ashx?v=320&s=n_majornews',
    'pv_date': 'Sat Aug 08 2020 00:02:41 GMT+0530 (India Standard Time)',
    'pv_count': '4',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'en-US,en;q=0.9',
}


main_page_response = requests.get(base_url, headers=headers, cookies=cookies)
main_soup = BeautifulSoup(main_page_response.content, 'html.parser')
homepage_soup = main_soup.select('div[id*="homepage"] table tr')[5]
data_dict = {}
for ele in homepage_soup.findAll('tr')[2:]:
    lis = [i.getText() for i in ele.findAll('td')]
    if lis[0] == search_text:
        data_dict['Ticker'] = lis[0]
        data_dict['Last'] = lis[1]
        data_dict['Change'] = lis[2]
        data_dict['Volume'] = lis[3]
        data_dict['Signal'] = lis[5]
        sub_url = base_url + ele.find('a')['href']
        subpage_response = requests.get(
            sub_url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(subpage_response.content, 'html.parser')
        table = soup.findAll("table", {"class": "snapshot-table2"})
        lis_elements = [i.getText() for i in table[0].findAll('td')]
        key = []
        value = []
        count = 1
        for a in lis_elements:
            if count % 2 != 0:
                key.append(a)
            else:
                value.append(a)
            count = count+1
        for i, j in zip(key, value):
            data_dict[i] = j
        print("Searched Term : "+search_text)
        print(data_dict)
        with open("finviz.json", "a") as outfile:
            json.dump(data_dict, outfile)
