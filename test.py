from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

#==============================================================================================
# !!!!!!!!!!!!!!!!!!!!!!!!!!! VARIABLES NEED TO BE UPDATED !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#==============================================================================================

baseurl = 'https://www.amaysim.com.au/my-account/my-amaysim'
username = "0468827174"
password = "theHoff34"
cfnumber = "0468827678"

loginxpaths = { 'usernameTxtBox' : "//input[@id='my_amaysim2_user_session_login']",
           'passwordTxtBox' : "//input[@id='password']",
           'submitButton' :   "//input[@name='commit']"
         }

homepagexpaths = { 'MySettings' : '//*[@id="menu_list"]/li[9]/a', 
           'MySettingsHeader' : '//*[@id="outer_wrap"]/div[2]/div[1]/h1',
           'CallForwarding' : '//*[@id="settings_call_forwarding"]/div',
           'CFEdit' : '//*[@id="edit_settings_call_forwarding"]' 
         }

CFxpaths = { 'CFHeader' : '//*[@id="body-content"]/div[15]', 
           'ConfirmBtn' : '//*[@id="body-content"]/div[15]/div/div/div/div[1]/a',
           'ForwardCallsTextBox' : '//*[@id="my_amaysim2_setting_call_divert_number"]',
           'SaveBtn' : '//*[@id="update_call_forwarding_form"]/div[4]/div/input',
           'SuccessModal' : '//*[@id="body-content"]/div[16]',
           'XSuccessModal' : '//*[@id="body-content"]/div[16]/a'
         }

driver = webdriver.Chrome()
# driver = webdriver.Firefox()
driver.get(baseurl + '/login')
driver.maximize_window()
delay = 10

#==============================================================================================
#==============================================================================================
#==============================================================================================

#Checking Login Page
try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, 'my_amaysim2_user_session_login')))
    print "Login Page"
except TimeoutException:
    print "Loading took too much time!"

#Clear Username TextBox if already allowed "Remember Me" 
driver.find_element_by_xpath(loginxpaths['usernameTxtBox']).clear()

#Write Username in Username TextBox
driver.find_element_by_xpath(loginxpaths['usernameTxtBox']).send_keys(username)

#Clear Password TextBox if already allowed "Remember Me" 
driver.find_element_by_xpath(loginxpaths['passwordTxtBox']).clear()

#Write Password in password TextBox
driver.find_element_by_xpath(loginxpaths['passwordTxtBox']).send_keys(password)

#Click Login button
driver.find_element_by_xpath(loginxpaths['submitButton']).click()

#==============================================================================================
#==============================================================================================
#==============================================================================================

#Checking Homepage
try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.ID, 'outer_wrap')))
    print "- Navigating Homepage"
except TimeoutException:
    print "Loading took too much time!"

driver.find_element_by_xpath(homepagexpaths['MySettings']).click()


#==============================================================================================
#==============================================================================================
#==============================================================================================

#Checking My Settings Page
try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, homepagexpaths['MySettingsHeader'])))
    print "-- Navigating My Settings"
except TimeoutException:
    print "Loading took too much time!"


try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, homepagexpaths['CallForwarding'])))
    print "--- Callforwarding"
except TimeoutException:
    print "Loading took too much time!"

CFvalue1 = driver.find_element_by_css_selector('#settings_call_forwarding > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)').text

try:
	assert CFvalue1 == 'No'
	print "---- Callforwarding value is No"
	# driver.execute_script("window.scrollBy(0,250)", "")
	# driver.find_element_by_xpath(homepagexpaths['CFEdit']).click()
except AssertionError:
    print "---- Callforwarding value is Yes"

#Click Edit button
driver.execute_script("window.scrollBy(0,1000)", "")

try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, homepagexpaths['CFEdit'])))
    print "--- Edit Callforwarding is Visibile"
except TimeoutException:
    print "Loading took too much time!"

driver.find_element_by_xpath(homepagexpaths['CFEdit']).send_keys(Keys.PAGE_DOWN)
driver.find_element_by_xpath(homepagexpaths['CFEdit']).click()
driver.find_element_by_link_text('Edit').click()

#==============================================================================================
#==============================================================================================
#==============================================================================================

#Checking My Settings Page
try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, CFxpaths['CFHeader'])))
    print "----- Call Forwarding Popup Confirmation"
except TimeoutException:
    print "Confirmation Pop up was not displayed"

#Click Confirm button
try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, CFxpaths['ConfirmBtn'])))
    print "----- Confirm button visible"
except TimeoutException:
    print "Confirm button was not displayed"

element = driver.find_element_by_link_text('Confirm')
driver.execute_script("arguments[0].click();", element)

#Call Forwarding number
driver.find_element_by_xpath(CFxpaths['ForwardCallsTextBox']).clear()
driver.find_element_by_xpath(CFxpaths['ForwardCallsTextBox']).send_keys(cfnumber)
driver.find_element_by_xpath('//*[@id="update_call_forwarding_form"]/div[2]/div/label[2]/span').click()

#Click SAVE button
try:
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, CFxpaths['SaveBtn'])))
    print "----- SAVE button visible"
except TimeoutException:
    print "Loading took too much time!"

callForwarding = driver.find_element_by_xpath(homepagexpaths['CallForwarding'])
saveBtn = driver.find_element_by_xpath(CFxpaths['SaveBtn'])
hover = ActionChains(driver).move_to_element(callForwarding).click().move_to_element(saveBtn).click().perform()

#Click Close button
driver.find_element_by_css_selector('.form_info_popup > a:nth-child(4)').click()

CFvalue2 = driver.find_element_by_css_selector('#settings_call_forwarding > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)').text

try:
	assert CFvalue2 == 'Yes'
	print "---- Callforwarding value is Yes"
except TimeoutException:
    print "---- Callforwarding value is No"

driver.quit()