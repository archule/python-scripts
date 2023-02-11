from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, NavigableString, Tag
import sys
from datetime import datetime
import re
from selenium.common.exceptions import TimeoutException


# Get additional Player information for player profile on NFL.com
def checkPlayerProfile(player):	

	# Set URL given that there are no special characters
	if (('.' not in player['first_name'] and '.' not in player['last_name']) and 
		('\'' not in player['first_name'] and '\'' not in player['last_name'])):		
		url = 'https://www.nfl.com/players/' + player['first_name'] + '-' + player['last_name'] + '/'

	# convert special characters to a dash
	else:

		first_name = ''
		last_name = ''

		name_checks = ['first_name', 'last_name']

		for i in range(len(name_checks)):

			if '.' in player[name_checks[i]] or '\'' in player[name_checks[i]]:

				parts = re.split('\.|\'', player[name_checks[i]])

				if parts[0] == '':
					parts.pop(0)
				if parts[-1] == '':
					parts.pop(-1)

				for j in range(len(parts)):

					if name_checks[i] == 'first_name':
						first_name = first_name + parts[j] 

						if (j + 1) != len(parts):
							first_name = first_name + '-'
						

					elif name_checks[i] == 'last_name' and (j + 1) != len(parts):
						last_name = last_name + (parts[j] + "-")
			else:
				if name_checks[i] == 'first_name':
					first_name = player['first_name']
				elif name_checks[i] == 'last_name':
					last_name = player['last_name']

		url =  'https://www.nfl.com/players/' + first_name + '-' + player['last_name'] + '/'


	# get URL
	browser.get(url)

	# wait for data 
	timeout = False
	try:
		WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "nfl-c-player-info__content")))
	except TimeoutException:
		timeout = True
	if not timeout:
		

		soup = BeautifulSoup(browser.page_source, "html.parser")

		# get desired data
		content = soup.find("div", {"class" : "nfl-c-player-info__content"})
		data = content.findAll("div")
		m = data


		for i in range(len(m)):
			if m[i] == "Height" and m[i+1] != '':
				player['height'] = m[i+1] 
			elif m[i] == "Weight" and m[i+1] != '':
				player['weight'] = m[i+1] 
			elif m[i] == "Arms" and m[i+1] != '':
				player['arms'] = m[i+1] 
			elif m[i] == "Hands" and m[i+1] != '':
				player['hands'] = m[i+1] 
			elif m[i] == "Age" and m[i+1] != '':
				years_past = int(datetime.now().year) - int(m[i+1])
				player['age'] = m[i+1] - years_past


# Get additional Player information for player combin3profile 
def checkPlayerCombineProfile(player, year):	

	url = player['player_info']
	browser.get(url)

	timeout = False

	try: 
		if year > 2021:
			print("ente1r")
			WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "css-moz91h")))
		else:
			print("enteer")
			WebDriverWait(browser, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "css-k9c8dc")))
	except TimeoutException:
		timeout = True
		print("enter6")

	if not timeout:
		print("enter")
		soup = BeautifulSoup(browser.page_source, "html.parser")

		if year > 2021:

			info = soup.find("div", {"class" : "css-moz91h"})

			data = info.find_all("div", {"class" : "css-w9rpyh"})


			combine_results = soup.find_all("div", {"class" : "css-1962qwu"})

			forty = combine_results[0].find("div", {"class" : "css-w1k723"}).text
			bench = combine_results[1].find("div", {"class" : "css-w1k723"}).text

			player['forty'] = forty
			player['bench'] = bench

			vertical = combine_results[2].find("div", {"class" : "css-w1k723"}).text
			broad = combine_results[3].find("div", {"class" : "css-w1k723"}).text

			player['vertical_jump'] = int(vertical)
			player['broad_jump'] = broad
			three_cone = combine_results[4].find("div", {"class" : "css-w1k723"}).text
			player['three_cone'] = three_cone


			twenty_yard_shuttle = combine_results[5].find("div", {"class" : "css-w1k723"}).text
			player['twenty_yard_shuttle'] = twenty_yard_shuttle

			sixty_yard_shuttle = combine_results[6].find("div", {"class" : "css-w1k723"}).text
			player['sixty_yard_shuttle'] = sixty_yard_shuttle
	

		scout_report = soup.find("div", {"class" : "css-k9c8dc"})

		for tag in scout_report:
			if isinstance(tag, NavigableString):
				continue
			tag.decompose()

		player['scout_report'] = scout_report.text
	


# Get additional Player information for player combin3profile 
def checkCombineData(players, year):	

	print("check players")
	for player in players:
		print("Set URL")
		url = 'https://www.pro-football-reference.com/draft/' + str(year) + '-combine.htm'

		print("Get URL")
		browser.get(url)

		print("begin wait")
		WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "table_wrapper")))
		print("end wait")
		soup = BeautifulSoup(browser.page_source, "html.parser")

		player_tag = player['last_name'] + ',' + player['first_name']

		print("check for --> " + str(player_tag))
		info = soup.find("th", {"csk" : player_tag})
		
		print("found info: " + str(info))
		row = info.parent

		print("add data")

		if row.find("td", {"data-stat" : "shuttle"}).text != "":
			player['twenty_yard_shuttle'] = row.find("td", {"data-stat" : "shuttle"}).text

		if row.find("td", {"data-stat" : "forty_yd"}).text != "":
			player['forty'] = row.find("td", {"data-stat" : "forty_yd"}).text

		if row.find("td", {"data-stat" : "vertical"}).text != "":
			player['vertical_jump'] = row.find("td", {"data-stat" : "vertical"}).text

		if row.find("td", {"data-stat" : "bench_reps"}).text != "":
			player['bench'] = row.find("td", {"data-stat" : "bench_reps"}).text

		if row.find("td", {"data-stat" : "broad_jump"}).text != "":
			player['broad_jump'] = row.find("td", {"data-stat" : "broad_jump"}).text

		if row.find("td", {"data-stat" : "cone"}).text != "":
			player['three_cone'] = row.find("td", {"data-stat" : "cone"}).text
	

		print("end add data")



# set current page of prospects
curr_page = 1

# get player year inputted on command line
year = 0

try:
	year = int(sys.argv[1])
except ValueError:
	"Please enter a number between "


ValueError

# data isn't going to be available
if year < 2014:
	print("This year is too early")
	quit()

# set URL
url = 'https://www.nfl.com/draft/tracker/prospects/all-positions/all-colleges/all-statuses/' + str(year) + '?page=' + str(curr_page)

# set browser
browser = webdriver.Chrome() #options=chrome_options

# go to URL
browser.get(url)

# wait until data loads
WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tbody")))

# create BeautifulSoup object
soup = BeautifulSoup(browser.page_source, "html.parser")

# Get table
table = soup.find('tbody')

# get table rows
y = soup.find_all('tr')

# create list of players
players = []

i = 1

print("Appendeding players from page " + str(curr_page))

# for each player row
while len(y[i].text) > 0 and i < 2:#len(y):


	# Get data from row
	data = y[i].find_all('td')

	# Get player combine page 
	player_info = data[0].a['href']

	# Name
	names = data[0].a.text.split()

	# college 
	college = data[0].find('div', class_="css-1ol443x").text

	# position
	position = data[2].text

	# class 
	class_ = data[4].text

	# rating 
	rating = data[5].text


	# Create a player with default values 
	player = {
		"first_name" : "N/A",
		"last_name" : "N/A",
		"college" : "N/A",
		"position" : "N/A",
		"player_info" "N/A"
		"class" : "N/A",
		"rating" : 0.00,
		"height" : "N/A",
		"weight" : 0.00,
		"arms" : "N/A",
		"hands" : 0.00,
		"age" : 0,
		"hometown" : "N/A",
		"forty" : 0.00,
		"bench" : 0,
		"vertical_jump": 0.00, 
		"broad_jump": 0.00, 
		"three_cone": 0.00,
		"twenty_yard_shuttle": 0.00,
		"sixty_yard_shuttle": 0.00,
		"scout_report" : "N/A",
		"year" : str(year)
	}

	# set gathered values 	
	if names[0] != '':
		player['first_name'] = names[0]
	if names[1] != '':
		player['last_name'] = names[1]
	if college != '':
		player['college'] = college
	if position !=  '':
		player['position'] = position
	if class_ != '':
		player['class'] = class_
	if rating != '':
		player['rating'] = float(rating)
	if player_info != '':
		player['player_info'] = player_info
	# add player to list of players
	players.append(player)
	i = i + 1


# get number of pages
x = soup.find('div', class_="css-13k5oh6").text.split()
page_num = int(x[3])

# while there are more pages of player prospects
while curr_page < 1: #page_num:

	# go to the next page 
	curr_page = curr_page + 1

	
	print("Working on page: " + str(curr_page) + " of " + str(page_num) + " pages")

	# update URL 
	url = 'https://www.nfl.com/draft/tracker/prospects/all-positions/all-colleges/all-statuses/' + str(year) + '?page=' + str(curr_page)

	# get the url 
	browser.get(url)

	# wait for player table to load
	WebDriverWait(browser, 30).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "tbody")))


	soup = BeautifulSoup(browser.page_source, "html.parser")

	# Get table
	table = soup.find('tbody')

	# get table rows
	y = soup.find_all('tr')

	i = 1

	

	# Loop through table rows 
	while len(y[i].text) > 0 and i < 2:#len(y):

		# Get desired data in table
		data = y[i].find_all('td')

		# Name
		names = data[0].a.text.split()

		# Get player combine page 
		player_info = data[0].a['href']

		# college 
		college = data[0].find('div', class_="css-1ol443x").text

		# position
		position = data[2].text

		# class 
		class_ = data[4].text

		# rating 
		rating = data[5].text


		# Create a player with default values 
		player = {
		"first_name" : "N/A",
		"last_name" : "N/A",
		"college" : "N/A",
		"position" : "N/A",
		"player_info" "N/A"
		"class" : "N/A",
		"rating" : 0.00,
		"height" : "N/A",
		"weight" : 0.00,
		"arms" : "N/A",
		"hands" : 0.00,
		"age" : 0,
		"hometown" : "N/A",
		"forty" : 0.00,
		"bench" : 0,
		"vertical_jump": 0.00, 
		"broad_jump": 0.00, 
		"three_cone": 0.00,
		"twenty_yard_shuttle": 0.00,
		"sixty_yard_shuttle": 0.00,
		"scout_report" : "N/A",
		"year" : str(year)
		}

		# set gathered values 	
		if names[0] != '':
			player['first_name'] = names[0]
		if names[1] != '':
			player['last_name'] = names[1]
		if college != '':
			player['college'] = college
		if position !=  '':
			player['position'] = position
		if class_ != '':
			player['class'] = class_
		if rating != '':
			player['rating'] = float(rating)
		if player_info != '':
			player['player_info'] = player_info

		players.append(player)
		i = i + 1

		

print("Appendin players")
for player in players:
	player.pop('player_info')

for player in players:
	checkPlayerProfile(player)
	#checkPlayerCombineProfile(player, year)

checkCombineData(players, year)




print(players)
