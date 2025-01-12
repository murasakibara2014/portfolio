import requests
from bs4 import BeautifulSoup
import json
import time
import csv

count = 143
for i in range(144, 203):
	url = f"https://book24.ru/catalog/russkoe-fentezi-2068/page-{i}/"

	headers = {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
			}
	q = requests.get(url, headers=headers)
	if q.status_code == 404:
		print(f"Достигнут конец: страница {url} не существует")
		break

	result = q.content

	soup = BeautifulSoup(result, "lxml")
	links = soup.find_all(class_="product-card__content")

	books = []
	for link in links:
		link = "https://book24.ru/" + link.find("a").get("href")
		req = requests.get(link, headers=headers)
		book_result = req.content
		soup = BeautifulSoup(book_result, "lxml")
		book_name = soup.find(class_="product-detail-page__title").text
		price = soup.find(class_="app-price product-sidebar-price__price").text
		characteristics = soup.find_all(class_="product-characteristic__item")

		labels = soup.find_all(class_="product-characteristic__label-holder")
		characteristics = {}

		# Извлекаем и очищаем метки и значения
		for label in labels:
			text = label.text.strip()  # Убираем лишние пробелы и переносы строк
			characteristics[text] = label.find_next_sibling().text.strip()

		# Извлекаем значения по ключам
		author = characteristics.get("Автор:", "Нет данных")
		series = characteristics.get("Серия:", "Нет данных")
		chapter = characteristics.get("Раздел:", "Нет данных")
		publishing_house = characteristics.get("Издательство:", "Нет данных")
		ISBN = characteristics.get("ISBN:", "Нет данных")
		age_limit = characteristics.get("Возрастное ограничение:", "Нет данных")
		year = characteristics.get("Год издания:", "Нет данных")
		page_amount = characteristics.get("Количество страниц:", "Нет данных")
		binding = characteristics.get("Переплет:", "Нет данных")
		paper = characteristics.get("Бумага:", "Нет данных")
		format_ = characteristics.get("Формат:", "Нет данных")
		weight = characteristics.get("Вес:", "Нет данных")
		
		book = {
			"Название": book_name,
			"Цена": price,
			"Автор": author,
			"Серия": series,
			"Раздел": chapter,
			"Издательство": publishing_house,
			"ISBN": ISBN,
			"Возрастное ограничение": age_limit,
			"Год издания": year,
			"Количество страниц":page_amount,
			"Переплет": binding,
			"Бумага": paper,
			"Формат": format_,
			"Вес": weight
			}

		books.append(book)
		time.sleep(0.2)

	with open("books.csv", "a", encoding="utf-8", newline="") as file:
		writer = csv.DictWriter(file, fieldnames=books[0].keys())
		writer.writeheader()
		writer.writerows(books)

	count += 1
	print(f"{count} is done")



