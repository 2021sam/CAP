#	Detect pop up window.

# pyautogui to the rescue
# https://www.geeksforgeeks.org/mouse-keyboard-automation-using-python/
# https://pynput.readthedocs.io/en/latest/keyboard.html
# https://pypi.org/project/schedule/
#	python3 -m venv env
# . activate

import time, schedule, os, pyautogui, smtplib
import credentials as c
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from pynput.keyboard import Key, Controller
from datetime import datetime


# import datetime
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains

keyboard = Controller()
driver = None

# successToday = False				# In case of a fail, will automatically run script.
# FailToday	= False

def removeFiles(path):
	os.chdir( path )
	for entry in os.scandir( path ):
		if entry.name.startswith('.'):
			continue
		# if entry.name.endswith('.mkv'):			#	Should not need to remove.  Set motion.conf to high so it never creates a video file.
		# 	continue
		# print( 'removeFiles → ' + entry.name )
		os.remove( entry.name )					#	Deletes all .jpg files, so in snapshot
												#	the first .jpg is the last is the one i need.


def checkFile( path, file ):
	os.chdir( path )
	c = 0
	found = False
	for entry in os.scandir( path ):
		c += 1
		print( '.' )
		if entry.name == file:
			found = True

	return found


def fileExist( path ):
	os.chdir( path )
	c = 0
	found = False
	for entry in os.scandir( path ):
		c += 1
		print( '.' )
		# if entry.name == file:
		# 	found = True

	return c



def zoom_out( j ):
	for i in range( j ):
		with keyboard.pressed(Key.ctrl):
			keyboard.press( '-' )
		time.sleep( 1 )



def reload():
	with keyboard.pressed(Key.ctrl):
		keyboard.press( 'r' )
	time.sleep( 5 )


def move_xy( x, y, step ):
	for i in range( 0, 300, step ):
		pyautogui.moveTo( x + i, y, duration = 1 )
		print( x + i )
		time.sleep( 2 )


def click( x, y ):
	pyautogui.moveTo( x, y, duration = 1 )
	pyautogui.click( x, y )
	time.sleep( 1 )


def setup():
	driver.get( c.bank_url )
	time.sleep( 2 )
	zoom_out( 5 )


def login():
	driver.find_element_by_id("oid").send_keys(c.username)
	time.sleep( 1 )
	driver.find_element_by_id("pass").send_keys(c.password)
	time.sleep( 1 )
	keyboard.press( Key.tab )
	keyboard.release( Key.tab )
	time.sleep( 1 )
	pyautogui.moveTo( 125, 390, duration = 1 )
	pyautogui.click( 125, 390 )
	time.sleep( 4 )


def select_account():
	zoom_out( 1 )
	time.sleep( 3 )
	# driver.find_element_by_partial_link_text(c.select_account).click()
	pyautogui.moveTo( 150, 420, duration = 1 )
	pyautogui.click( 150, 420 )
	# time.sleep( 12 )			#	Takes a while to load next page.		10.22.2021 Needed more time
	time.sleep( 15 )


def download():
	zoom_out( 1 )
	time.sleep( 5 )
	keyboard.press( Key.page_down )
	keyboard.release( Key.page_down )
	time.sleep( 1 )
	keyboard.press( Key.page_down )
	keyboard.release( Key.page_down )
	time.sleep( 2 )
	# keyboard.press( Key.up )
	# keyboard.release( Key.up )
	keyboard.press( Key.down )		# 11/20/2021  Now you need to key down.
	keyboard.release( Key.down )

	time.sleep( 2 )
	screen_shot()
	pyautogui.moveTo( 542, 226, duration = 1 )
	pyautogui.click( 542, 226 )							# 11/20/2021  Click on Download Link
	time.sleep( 1 )

	# driver.find_element_by_class_name('export-trans-view download-upper').click()
	# print('ada-hidden')
	# driver.find_element_by_class_name('ada-hidden').click()
	# time.sleep( 10 )
	# print('Download')
	# driver.find_element_by_link_text('Download').click()




	keyboard.press( Key.tab )
	keyboard.release( Key.tab )
	time.sleep( 1 )

	#	If first of new period → 26th of every month.
	day = datetime.today().day
	if day == 26:
		keyboard.press( Key.down )
		keyboard.release( Key.down )

	time.sleep( 1 )
	keyboard.press( Key.tab )
	keyboard.release( Key.tab )
	time.sleep( 1 )
	keyboard.press( 'M' )
	keyboard.release( 'M' )

	time.sleep( 1 )
	keyboard.press( Key.tab )
	keyboard.release( Key.tab )

	time.sleep( 1 )
	keyboard.press( Key.enter )
	keyboard.release( Key.enter )

	time.sleep( 7 )



def close_browser():
	# pyautogui.moveTo( 696, 53, duration = 1 )
	# pyautogui.click( 696, 53 )
	# with keyboard.pressed(Key.ctrl):
	# 	with keyboard.pressed(Key.shift):
	# 		keyboard.press( 'W' )
	with keyboard.pressed(Key.ctrl):
		keyboard.press( 'w' )




def update_cap():
	global driver

	driver.get(c.domain_url)
	time.sleep( 3 )
	# zoom_out( 5 )

	id = 'id_username'
	if driver.find_elements_by_css_selector( id ):
		print ( f'Element exists: {id}' )


	driver.find_element_by_id("id_username").send_keys( c.cap_admin_user_name )
	driver.find_element_by_id("id_password").send_keys( c.cap_admin_user_pass )
	time.sleep( 1 )
	driver.find_element_by_xpath('//button[contains(text(), "Welcome")]').click()

	time.sleep( 1 )
	driver.get( f'http://{wan_server_ip}:{server_port}/ie/upload' )
	time.sleep( 2 )
	# driver.find_element_by_xpath('//button[contains(text(), "Choose File")]').click()

	click( 60, 291 )
	click( 75, 241 )
	click( 665, 459 )
	driver.find_element_by_id('cc').click()
	# click( 19, 451 )

	driver.find_element_by_xpath('//button[contains(text(), "Upload")]').click()
	# close_browser()

	time.sleep( 10 )
	results = driver.find_element_by_id('results').text
	print( results )
	# print( pyautogui.position() )
	return results
	# time.sleep( 10 )
	# print( pyautogui.position() )
	#
	# time.sleep( 10 )
	# print( pyautogui.position() )
	#
	# time.sleep( 10 )
	# print( pyautogui.position() )



def log():
	pass


def notify(type, subject, body):
	print('notify')
	recipients = c.recipients
	msg = MIMEMultipart()
	msg['From'] = c.server_email_address
	msg['To'] =  ", ".join( c.recipients )
	# print('body = {}'.format( body ))
	msg['Subject'] = subject
	msg.attach(MIMEText(body, 'plain'))
	text = msg.as_string()
	email_server = smtplib.SMTP('smtp.gmail.com', 587)
	email_server.starttls()
	email_server.login(c.server_email_address, c.server_email_password)
	email_server.sendmail(c.server_email_address, c.recipients, text)
	email_server.quit()


def get_date():
	from datetime import date
	todays_date = date.today()
	print("Current date: ", todays_date)
	# return todays_date

	# fetching the current year, month and day of today
	print("Current year:", todays_date.year)
	print("Current month:", todays_date.month)
	print("Current day:", todays_date.day)
	return [ todays_date.year, todays_date.month, todays_date.day ]


def get_time():
	h = datetime.now().hour
	m = datetime.now().minute
	s = datetime.now().second
	return [h, m, s]


def screen_shot():
	os.chdir( '/home/pi/Desktop/cap/shots' )    # Windows
	# shot = f'{ image_datetime.now() }.png'

	date = get_date()
	time = get_time()
	shot = f'shot_{ date[0] }-{ date[1] }-{ date[2] }_{ time[0] }-{ time[1] }-{ time[2] }.png'

	print( os.getcwd() )
	print( shot )
	screenshot = driver.save_screenshot( shot )

def tasks():
	global driver

	driver = webdriver.Chrome( executable_path = '/usr/lib/chromium-browser/chromedriver' )

	removeFiles( '/home/pi/Downloads' )
	setup()
	login()
	screen_shot()

	reload()			#	In case pop up.  Need to add if popup exists

	select_account()
	screen_shot()
	download()
	screen_shot()

	success = fileExist( '/home/pi/Downloads/' )		# return either 0 or 1
	print( f'success = { success }' )
	if not success:
		print( f'{ datetime.now() } - Not able to download.')
		notify( 0, 'Auto BoA Update', 'Not able to download.' )

	if success:
		results = update_cap()
		print( f'{ datetime.now() } - Success !')
		notify( 1, 'Auto BoA Update', results )

	close_browser()
	successToday = True



def link():
	global driver

	driver = webdriver.Chrome( executable_path = '/usr/lib/chromium-browser/chromedriver' )
	driver.get( f'http://{wan_server_ip}:{cap_server_port}/link/auto' )
	time.sleep( 10 )
	results = driver.find_element_by_id('results')
	print( results.text )
	print( f'{ datetime.now() } - Scheduled Link')
	notify( 1, 'Auto BoA Link', results.text )
	close_browser()



schedule.every().monday.at("06:00").do( tasks )
schedule.every().tuesday.at('06:00').do( tasks )
schedule.every().wednesday.at("06:00").do( tasks )
schedule.every().thursday.at("06:00").do( tasks )
schedule.every().friday.at("06:00").do( tasks )

schedule.every().monday.at("20:00").do( link )
schedule.every().tuesday.at('20:00').do( link )
schedule.every().wednesday.at("20:00").do( link )
schedule.every().thursday.at("20:00").do( link )
schedule.every().friday.at("20:00").do( link )


# schedule.every(1).minutes.do( tasks )
# schedule.every().wednesday.at("08:45").do( tasks )

# tasks()
# link()
while True:
	schedule.run_pending()
	time.sleep(1)
