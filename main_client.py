'''
This is a proof-of-concept program to show how one might log into
the SJHS portals page. I chose to use a webdriver over traditional
webscraping in order to be able to parse grade/class data from a
table that is loaded by JavaScript.

I will probably implement this function in a future project I make.
I hope someone finds this useful, either now or in coming years,
as it really was a pain trying to do this without a driver.

	author: Jack Donofrio
	date: 9:27 PM, April 10, 2020
'''

from selenium import webdriver
from Course import Course
import time

USERNAME = '' # Your school email
PASSWORD = '' # Your password
# These words appear in classes that should never have grades.
BLACKLIST_KEYWORDS = ['Lab', 'Homeroom','Service','Study', 'JrCollPlan'] # need to determine others
# note: 'Lab' accounts for AP Chem/Bio block lab period, which gets its own portals entry

driver = webdriver.Firefox() # You could use a headless drivervv also

driver.get('https://www.plusportals.com/sjhs') # load page

# Locate user/pass forms
username = driver.find_element_by_id('UserName')
password = driver.find_element_by_id('Password')

# Send constant user/pass values to defined forms
username.send_keys(USERNAME)
password.send_keys(PASSWORD)

# Clicks the 'Sign In' button
driver.find_element_by_name('btnsumit').click()

# must wait so javascipt can load grade data into table from portals servers
time.sleep(6)

# access table that contains grades / classes by its xpath
table = driver.find_element_by_xpath('//*[@id="GridProgress"]/div[2]/table/tbody')

# split up table into a list, rows, based on location of newline
rows = table.text.split('\n')

# Remove all rows containing blacklisted keywords
for i in range(len(rows)):	
	for keyword in BLACKLIST_KEYWORDS:
		if i < len(rows) and keyword in rows[i]:
			rows.remove(rows[i])

# counts the number of digits in a given string
def count_digits(str):
	count = 0
	for ch in str:
		if ch.isdigit():
			count += 1
	return count

course_list = [] # List of Course objects

# extracts the course name and grade from each class. assigns 'none posted'
# to classes without a grade. 
for row in rows:
	course_name = row[0:15]
	digit_count = count_digits(row)
	if digit_count <= 6 and '.' not in row or count_digits(row[-3:]) == 0:
		grade = 'none posted'
	else:
		grade = row[-3:].strip()
	course_list.append(Course(course_name, grade))
	print(f"CLASS: {course_name}, GRADE: {grade}")
driver.close()
'''
There are likely some bugs here I need to squash.
The little algorithm above, especially, will likely need some work,
as it is tailored specifically to my schedule.
'''