import requests
from bs4 import BeautifulSoup
import json
import time


persons_url_list = []
for i in range(0, 740, 20):
	url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}"

	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
			}
	q = requests.get(url)
	result = q.content

	soup = BeautifulSoup(result, "lxml")
	persons = soup.find_all(class_="bt-slide-content")

	for person in persons:
		person_page_url = person.find("a").get("href")
		persons_url_list.append(person_page_url)

with open("persons_url_list.txt", "w", encoding="utf-8") as file:
	for line in persons_url_list:
		file.write(f"{line}\n")

with open("persons_url_list.txt") as file:
	lines = [line.strip() for line in file.readlines()]

	data_dict = []
	count = 0
	for line in lines:
		q = requests.get(line)
		result = q.content

		soup = BeautifulSoup(result, "lxml")
		person = soup.find(class_="col-xs-8 col-md-9 bt-biografie-name").text
		person_name_company = person.strip().split(",")
		person_name = person_name_company[0]
		person_company_full = person_name_company[1]
		person_company = person_company_full.split("\n")[0]
		social_networks = soup.find(class_="bt-linkliste").find_all(class_="bt-link-extern")
		social_networks_urls = []
		for item in social_networks:
			social_networks_urls.append(item.get("href"))
		data = {
			"person_name": person_name,
			"person_company": person_company,
			"social_networks": social_networks_urls
		}
		count += 1
		print(f"{count}: {line} is done") 

		data_dict.append(data)

		with open("data.json", "w", encoding="utf-8") as json_file:
			json.dump(data_dict, json_file, indent=4)

		time.sleep(2)






