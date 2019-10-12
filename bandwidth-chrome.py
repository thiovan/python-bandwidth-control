import time
import sys
import logging
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

url = "http://192.168.100.99/login.html"
timeout = 30
downLimitVar = 1000
upLimitVar = 500
myDeviceName = ["Thio-PC", "Thio-Phone", "Thio-Alcatel"]

dateTime = datetime.datetime.now()
log_dir = os.getcwd()
log_fname = log_dir + "\\logs\\" + dateTime.strftime("%d-%m-%Y") + ".log"
logging.basicConfig(
    filename=log_fname,
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

options = Options()
options.add_argument("--window-size=1366,768")
options.add_argument("--start-maximized")
options.add_argument("--headless")
options.add_argument("log-level=3")
browser = webdriver.Chrome(
    options=options,
    executable_path=r"D:\Bandwidth Control\chromedriver.exe",
    service_log_path=r"NUL"
)
browser.get(url)


def logInfo(message):
    print(message)
    logging.info(message)


def findElement(browser, timeout, by, element):
    logInfo("Finding element " + element)
    try:
        element_present = EC.presence_of_element_located((by, element))
        return WebDriverWait(browser, timeout).until(element_present)
    except TimeoutException:
        logInfo("Timed out waiting for page to load")
        browser.quit()
        sys.exit()


logInfo("----Process Start----")

pass_elem = findElement(browser, timeout, By.ID, "login-password")
pass_elem.send_keys("syntaxerror")

btn_login_elem = findElement(browser, timeout, By.ID, "save")
btn_login_elem.click()

time.sleep(1)

menu_bw_elem = findElement(browser, timeout, By.ID, "net-control")
menu_bw_elem.click()

time.sleep(2)

table_bw = findElement(browser, timeout, By.ID, "qosList")
table_row_list = table_bw.find_elements_by_tag_name("tr")

for row in table_row_list:
    deviceName = row.find_elements_by_tag_name("td")[0]
    deviceName = deviceName.find_elements_by_tag_name("div")[0].text

    if deviceName not in myDeviceName:
        downLimit = row.find_elements_by_tag_name("td")[3]
        downLimit = downLimit.find_elements_by_tag_name("input")[0]
        formattedDownLimitVar = str(downLimitVar) + ".00KB/s"
        if downLimit.get_attribute("value") != formattedDownLimitVar:
            logInfo("Set download limit to " +
                    formattedDownLimitVar + " for device " + deviceName)
            downLimit.clear()
            downLimit.send_keys(downLimitVar)

        upLimit = row.find_elements_by_tag_name("td")[4]
        upLimit = upLimit.find_elements_by_tag_name("input")[0]
        formattedUpLimitVar = str(upLimitVar) + ".00KB/s"
        if upLimit.get_attribute("value") != formattedUpLimitVar:
            logInfo("Set upload limit to " +
                    formattedUpLimitVar + " for device " + deviceName)
            upLimit.clear()
            upLimit.send_keys(upLimitVar)

btn_save_elem = findElement(browser, timeout, By.ID, "submit")
btn_save_elem.click()
time.sleep(3)
browser.quit()
logInfo("----Process Done----")
