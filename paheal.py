from bs4 import BeautifulSoup as BS
import requests
import os
import random

tags = []

hdr = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
	'Accept-Encoding': 'none',
	'Accept-Language': 'en-US,en;q=0.8',
	'Connection': 'keep-alive'
}

def getImageIndex(dir):
	i = len(os.listdir(os.getcwd()+"/"+dir))
	return i

def downloadImage(link, list):
	list = list.split("%20")
	imageIndex = getImageIndex(",".join(list))
	imagePage = requests.get("https://rule34.paheal.net"+link, headers=hdr)	
	imagePage = BS(imagePage.text)
	title = imagePage.find("input", {"class": "autocomplete_tags"})
	image = imagePage.find("img", {"class": "shm-main-image"})
	image = requests.get(image['src'], headers=hdr)
	open(os.getcwd()+"/"+",".join(list)+"/"+str(imageIndex)+".png", "wb").write(image.content)
	print("download images...(this could take a while)")

def calculatePages(taglist):
	for v in range(500):
		scrapePage = requests.get("https://rule34.paheal.net/post/list/"+taglist+"/"+str(v), headers=hdr)
		scrapePage = BS(scrapePage.text)
		scrapeImages = scrapePage.findAll("a", {"class": "shm-thumb-link"})
		for k in range(len(scrapeImages)):
			downloadImage(scrapeImages[k]['href'], taglist)

def main():
	print("Please enter the tags you want to scrape(separate with a comma):")
	tags = input()
	if not os.path.isdir(os.getcwd()+"/"+tags):
		os.mkdir(os.getcwd()+"/"+tags)
	tags = tags.split(",")
	calculatePages("%20".join(tags))
main()