import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
query = 'fiber optics'
number_result = 3
ua = UserAgent()

google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
response = requests.get(google_url, {"User-Agent": ua.random})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div')

import pdb

pdb.set_trace()

links = []
titles = []
descriptions = []
for r in result_div:
    # Checks if each element is present, else, raise exception
    try:
        link = r.find('a', href=True)
        title = r.find('h3').get_text()
        description = r.find('span').get_text()

        # Check to make sure everything is present before appending
        if link != '' and title != '' and description != '':
            links.append(link['href'])
            titles.append(title)
            descriptions.append(description)
    # Next loop if one element is not present
    except:
        continue

print(links)
print(titles)
print(descriptions)