import re
import requests
from bs4 import BeautifulSoup


def link_scraping(question_description):
    link_list = []
    page = requests.get("https://www.google.dz/search?q=" + question_description)
    soup = BeautifulSoup(page.content)
    for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        link_list.append(re.split(":(?=http)", link["href"].replace("/url?q=", "")))
    return link_list[:4]
