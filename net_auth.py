from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options


def net_auth(netauth_addr,netauth_name,netauth_passwd):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    try:
        browser = webdriver.Chrome(chrome_options=chrome_options)
    except Exception as e:
        print("can not open Chrome",e)
        return e
    else:
        browser.get(netauth_addr)
        sleep(1)
    try:
        username = browser.find_element_by_name('username')
        passwd = browser.find_element_by_name('password')
        login = browser.find_element_by_id('login')
    except Exception as e:
        print("objects are not found",e)
        return e
    else:
        username.send_keys(netauth_name)
        passwd.send_keys(netauth_passwd)
        login.click()
        sleep(1)
    #finally:
    #    browser.quit()
    try:
        ip = browser.find_element_by_id('ip')
    except Exception as e:
        print("login error",e)
        return e
    else:
        ipaddr = ip.text
        browser.quit()
        return ipaddr
    finally:
        browser.quit()