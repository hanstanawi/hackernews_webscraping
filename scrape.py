import requests
from bs4 import BeautifulSoup
import pprint
import csv
import json


def init(link):
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = {
        'links': soup.select('.storylink'),
        'subtext': soup.select('.subtext')
    }
    return content


page_1 = init('https://news.ycombinator.com/news')
page_2 = init('https://news.ycombinator.com/news?p=2')

mega_links = page_1['links'] + page_2['links']
mega_subtext = page_1['subtext'] + page_2['subtext']


def sorted_news(hn_list):
    return sorted(hn_list, key=lambda k: k['Votes'], reverse=True)


def create_custom(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        author = subtext[idx].select('.hnuser')[0].getText()
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({
                    'Title': title,
                    'Link': href,
                    'Votes': points,
                    'Author': author
                })
    return sorted_news(hn)


result = create_custom(mega_links, mega_subtext)
pprint.pprint(result)


# CSV Write
csv_columns = ['Title', 'Link', 'Votes', 'Author']
csv_file = "News.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in result:
            writer.writerow(data)
except IOError:
    print("I/O error")

# JSON write
with open('news.json', 'w') as json_write:
    json.dump(result, json_write)
