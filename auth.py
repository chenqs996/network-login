from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options

netauth_addr = "http://10.248.98.2/"

netauth_nanme = "19S152095"

netauth_passwd = "19961231"


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get(netauth_addr)

username = browser.find_element_by_name('username')
passwd = browser.find_element_by_name('password')
login = browser.find_element_by_id('login')

username.send_keys(netauth_nanme)
passwd.send_keys(netauth_passwd)
login.click()
sleep(1)
ip = browser.find_element_by_id('ip')
print(ip)
print(ip.text)