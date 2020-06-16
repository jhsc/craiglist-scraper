from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
import csv

headers = ({
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
})

url = 'https://losangeles.craigslist.org/search/cpg?'
print("Calling url = " + url)
r = get(url, headers=headers)
keywords = ['developer', 'dev', 'app', 'application', 'mobile',
            'software', 'devops', 'server', 'api', 'database', 'code']
data = []

page_html = BeautifulSoup(r.text, 'html.parser')

content = page_html.find_all('li', class_="result-row")
if content != []:
	for row in content:
		info = row.find_all('a')[1]
		title = info.text or ""
		if any(word in title.lower() for word in keywords):
			time = row.find_all('time')[0]
			d = ({
				'date': time.get('datetime'),
				'title': info.text,
				'href': info.get('href')
			})
			data.append(d)

if len(data) > 0:
	csv_file = datetime.now().ctime() + '.csv'
	csv_columns = ['date', 'title', 'href']
	try:
		with open(csv_file, 'w') as csvfile:
			writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
			writer.writeheader()
			for row in data:
				writer.writerow(row)
	except IOError:
		print('I/O error')
