import time
from datetime import datetime, timedelta

import schedule
import yaml
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def book_class() -> None:
    
    # Start driver
    driver = webdriver.Chrome()
    driver.set_window_size(1400,1000)
    driver.get(url)

    # Login
    try:
        # fill email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#login"))
        )
        email_input.send_keys(email)

        # fill password
        pw_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
        )
        pw_input.send_keys(pw)

        # click login button
        driver.find_element(By.CSS_SELECTOR, "#but_dados").click()

    except:
        print("Login didn't work")

    # Go to classes calendar view
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR, "#feed_minhas_aulasxxx > div > div > div.card-footer > a").click()
    driver.implicitly_wait(10)

    # Find the date of today + 3 days
    today = driver.find_elements(By.CLASS_NAME, "calendar-day-today")[0]
    today_date = today.get_attribute("data-date")
    date_object = datetime.strptime(today_date, '%Y-%m-%d').date()

    target_date = date_object + timedelta(days=1)
    target_date_str = '{0.year}-{0.month}-{0.day}'.format(target_date)
    
    # Select and click the correct day
    days = driver.find_elements(By.CLASS_NAME, "calendar-day")

    for day in days:
        if day.get_attribute("data-date") == target_date_str:
            driver.implicitly_wait(10)

            if day.is_displayed():
                day.click()
                break
    
    # Enroll in the first class of the day
    button = driver.find_elements(By.CLASS_NAME, "button")[0]

    if button.is_displayed():
        button.click()

# Constant variables
url = "https://www.regybox.pt/app/app_nova/login.php?id_box=204&lang=&type="

# Get credentials
cred = yaml.safe_load(open("login_credentials.yml", "r"))
email = cred['regybox_user']['email']
pw = cred['regybox_user']['password']

schedule.every().day.at("06:00:30").do(book_class)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(60)