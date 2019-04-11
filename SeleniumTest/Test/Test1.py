from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome(r"..\drivers\chromedriver.exe")
driver.set_page_load_timeout(10)
driver.get("http://ericpak.dev.s3-website-us-west-2.amazonaws.com/#/")

def add_fortune(fortune, author):
    try:
        driver.find_element_by_id("add-fortune-button").send_keys(Keys.ENTER)
        driver.find_element_by_id("form-fortune-edit-input").send_keys(fortune)
        driver.find_element_by_id("form-author-edit-input").send_keys(author)
        driver.find_element_by_xpath('//button[text()="Submit"]').click()
    except Exception as e:
        print(e)

def add_fortune_approve(fortune, author):
    try:
        driver.find_element_by_id("add-fortune-button").send_keys(Keys.ENTER)
        driver.find_element_by_id("form-fortune-edit-input").send_keys(fortune)
        driver.find_element_by_id("form-author-edit-input").send_keys(author)
        driver.find_element_by_xpath('//*[@id="form-checks"]/div/label').click()
        driver.find_element_by_xpath('//button[text()="Submit"]').click()
    except Exception as e:
        print(e)

def add_fortune_then_approve(fortune, author):
    try:
        driver.find_element_by_id("add-fortune-button").send_keys(Keys.ENTER)
        driver.find_element_by_id("form-fortune-edit-input").send_keys(fortune)
        driver.find_element_by_id("form-author-edit-input").send_keys(author)
        driver.find_element_by_xpath('//*[@id="form-checks"]/div/label').click()
        driver.find_element_by_xpath('//button[text()="Submit"]').click()
        wait = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div[1]/div/table/tbody//td[text()="%s"]' % fortune))
        )
        targetTD = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/table/tbody//td[text()="%s"]' % fortune)
        targetTR = targetTD.find_element_by_xpath('./..')
        targetBUTTON = targetTR.find_element_by_xpath('./td[4]/button[1]')
        targetBUTTON.click()
    except Exception as e:
        print(e)

def add_fortune_then_approve_twice(fortune, author):
    try:
        driver.find_element_by_id("add-fortune-button").send_keys(Keys.ENTER)
        driver.find_element_by_id("form-fortune-edit-input").send_keys(fortune)
        driver.find_element_by_id("form-author-edit-input").send_keys(author)
        driver.find_element_by_xpath('//*[@id="form-checks"]/div/label').click()
        driver.find_element_by_xpath('//button[text()="Submit"]').click()
        wait = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div[1]/div/table/tbody//td[text()="%s"]' % fortune))
        )
        targetTD = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/table/tbody//td[text()="%s"]' % fortune)
        targetTR = targetTD.find_element_by_xpath('./..')
        targetBUTTON = targetTR.find_element_by_xpath('./td[4]/button[1]')
        targetBUTTON.click()
        targetBUTTON.click()
    except Exception as e:
        print(e)

def delete_fortune(fortune):
    try:
        wait = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div[1]/div/table/tbody//td[text()="%s"]' % fortune))
        )
        targetTD = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div/table/tbody//td[text()="%s"]' % fortune)
        targetTR = targetTD.find_element_by_xpath('./..')
        targetBUTTON = targetTR.find_element_by_xpath('./td[4]/button[2]')
        targetBUTTON.click()
    except Exception as e:
        print(e)

#################################################
# Testing normal add of a fortune.
#################################################

try:
    add_fortune("Test Fortune", "Selenium")
    delete_fortune("Test Fortune")
except Exception as e:
    print(e)

#################################################
# Testing add of a fortune with a blank fortune.
#################################################

#add_fortune("", "Selenium")
#delete_fortune("")

#################################################
# Testing add of a fortune without an author.
#################################################

#add_fortune("Test Fortune", "")
#delete_fortune("Test Fortune")

#################################################
# Testing add of a fortune without both fields.
#################################################

#add_fortune("", "")
#delete_fortune("")

#################################################
# Add fortune and check the approve checkbox.
#################################################

#add_fortune_approve("Test Fortune", "Selenium")
#time.sleep(2)
#delete_fortune("Test Fortune")

#################################################
# Add fortune and click the approve button.
#################################################

#add_fortune_then_approve("Test Fortune", "Selenium")
#time.sleep(2)
#delete_fortune("Test Fortune")

#################################################
# Add fortune and click the approve button twice.
#################################################

add_fortune_then_approve_twice("Test Fortune", "Selenium")
time.sleep(2)
delete_fortune("Test Fortune")

#################################################

time.sleep(3)
driver.quit()