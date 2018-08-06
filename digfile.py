# library imports
from bs4 import *
import requests

# List to stores Links from google search page
sites = []
movies = []
googleallpages = [] # List to store next 9 pages of google search

#File valid extensions (file links should end with these extensions)
ext = ('mkv','mov','avi','mp4','mpg','wmv')

# Browser Headers
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

#Name of file to be searched - Search Term
name = input("Enter a movie name : ")

# URL Prefix
urlPref = "https://www.google.com/search?q="

# URL Suffix
urlSuff = "%20%2B(mkv%7Cmp4%7Cavi%7Cmov%7Cmpg%7Cwmv)%20-inurl%3A(jsp%7Cpl%7Cphp%7Chtml%7Caspx%7Chtm%7Ccf%7Cshtml)%20intitle%3Aindex.of%20-inurl%3A(listen77%7Cmp3raid%7Cmp3toss%7Cmp3drug%7Cindex_of%7Cwallywashis)"

# complete URL of first search page
url1 = urlPref + name + urlSuff

soup = ' '
#Function to find and append the websites on a google search page into sites[] list
def getResLinks(url):
	# Get URL page data
	page = requests.get(url, headers=headers)
	# Get page data parsed as HTML
	global soup
	soup = BeautifulSoup(page.text, "html.parser")
	#Scraping google searchpage links
	links = soup.findAll("cite")
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~ WEB FOLDER LINKS ~~~~~~~~~~~~~~~~~~~~~~~~")
	for getL in links:
		hrefs = getL.get_text()
		sites.append(hrefs)
		print(hrefs)

#function to find next 9 search pages of google and store them in googleallpages[] list
def googlekpages():
	flclasslinks = []
	nextpage = soup.find_all("a",class_="fl")
	for pages in nextpage:
		pg = (pages['href'])
		pg = 'http://google.com' + pg
		flclasslinks.append(pg)
	global googleallpages
	googleallpages = (flclasslinks[-9:])

#Function to check whether the Search term is present in final file link. It'll return 1 if matches else skip the link.
def match(filekalink, searchterm):
	delimiters = {'%20','%5','_','.','-','/',':','%','(',')','{','}','[',']'}
	filekalink = filekalink.lower()
	searchterm = searchterm.lower()
	for delimiter in delimiters:
		filekalink = filekalink.replace(delimiter,' ')
	filekalink = filekalink.split(' ')
	if set(searchterm.split(' ')).issubset(filekalink) :
		return 1


def getMovielink(websites):
	print("~~~~~~~~~~~~~~~~~~~~~~~~ MOVIE LINKS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	for site in websites:
		if ((site.startswith("https://")) or (site.startswith("http://"))):
			fullsitelink = site
		else :
			fullsitelink = "http://" + site
		try :
			innersite = requests.get(fullsitelink, headers=headers)
			innersoup = BeautifulSoup(innersite.text, "html.parser")
			alllinks = innersoup.findAll("a")
			for movielink in alllinks:
				movie = (movielink['href'])
				milgaya = fullsitelink + movie
				#if milgaya.endswith(('mkv','mov','avi','mp4','mpg','wmv')) : ----depricated
				if milgaya.endswith(ext) :
					if match(milgaya, name) == 1:
						print(milgaya)
		except :
			continue


getResLinks(url1)
getMovielink(sites)

ask = input("Want more links? (Y/N)")
if ask == 'Y':
	googlekpages()
	print(googleallpages)
	for page in googleallpages:
		getResLinks(page)
	for onesite in sites:
		getMovielink(sites)



