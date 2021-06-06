import requests
from fake_useragent import UserAgent, FakeUserAgentError
from lxml import html
from multiprocessing import Pool
from functools import partial
import csv

def get_content(url):
    try:
        ua = UserAgent()
    except FakeUserAgentError as ex:
        print(ex)

    headers = {'accept': '*/*', 'user-agent': ua.firefox}
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.text
    else:
        print('Connection Error' + str(r.status_code))
        return ''

def get_links(url, xpath):
    content = get_content(url)
    parsed_content = html.fromstring(content)
    links = parsed_content.xpath(xpath)
    print(links)
    return links

def links_writer(torrent_links):
    links_data_file = open('links-erai-raws.csv', 'w')
    
    with links_data_file as links:
        writer = csv.writer(links)
        writer.writerows(torrent_links)
    
    print('Links saved')

def main():
    anime = get_links('https://www.erai-raws.info/anime-list/', '//div[@class="ind-show button button5"]/a/@href')
    p = Pool(processes=50)
    get_links_partial = partial(get_links, xpath = '//a[@class="load_more_links"]/@href') # Create new function get_links_partial() with first argument X and second Y fixed (xpath)
    torrent_links = p.map(get_links_partial, ['https://www.erai-raws.info/anime-list/' + a for a in anime])
    links_writer(torrent_links)
    print(len(anime))
    
if __name__ == '__main__':
    main()