from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'
    def tearDown(self):
        self.driver.quit()
    
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/login/"]')
        login.click()
        time.sleep(2)
        email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email.send_keys("waremo9428@twugg.com")
        password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password.send_keys("Sample@123")
        time.sleep(2)
        submit = driver.find_element(By.CSS_SELECTOR, 'button#login.btn.btn-primary.btn-block.register-btn')
        submit.click()
        time.sleep(2)
        driver.get("http://127.0.0.1:8000/register_webinar/")
        time.sleep(3)
        title = driver.find_element(By.NAME, "title")
        title.send_keys("Webinar on Global Warming")

        fee = driver.find_element(By.NAME, "fee")
        fee.send_keys("100")  # You can change this value

        start_time = driver.find_element(By.NAME, "start_time")
        start_time.send_keys("09:00 AM")  # Adjust the time as needed

        end_time = driver.find_element(By.NAME, "end_time")
        end_time.send_keys("11:00 AM")  # Adjust the time as needed

        date = driver.find_element(By.NAME, "date")
        date.send_keys("26-11-2023")  # Use the desired date

        deadline = driver.find_element(By.NAME, "deadline")
        deadline.send_keys("23-11-2023")  # Use the desired date

        event_type = driver.find_element(By.NAME, "event_type")
        event_type.send_keys("Online")  # Or "Offline" if needed

        # Depending on the event type, you can handle the "Livestream Link" and "Location" fields here

        organizer_name = driver.find_element(By.NAME, "organizer_name")
        organizer_name.send_keys("Dept. of Environment Studies")

        phone_number = driver.find_element(By.NAME, "phone_number")
        phone_number.send_keys("8978537890")  # Use the desired phone number

        poster = driver.find_element(By.NAME, "poster")
        poster.send_keys("https://example.com/poster.jpg")  # Use the desired image URL

        max_participants = driver.find_element(By.NAME, "max_participants")
        max_participants.send_keys("100")  # Set the maximum number of participants
        # Find the "Speakers" section and its elements
        speakers_container = driver.find_element(By.ID, "speakers-container")
        speaker_designation = driver.find_element(By.NAME, "speakers_designation[]")
        speaker_name = driver.find_element(By.NAME, "speakers_name[]")

        # Fill in speaker information
        speaker_designation.send_keys("Mr")  # You can change the designation
        speaker_name.send_keys("John Kim")  # Enter the speaker's name


        # For the "Speakers" section, you can add speakers dynamically if needed.

        description = driver.find_element(By.NAME, "description")
        description.send_keys("Are you concerned about the pressing issue of global warming and its far-reaching consequences? Join us for an insightful webinar where we dive deep into the science, impact, and sustainable solutions related to this critical environmental challenge.")
        time.sleep(3)
        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()
        time.sleep(3)
        driver.get("http://127.0.0.1:8000/listwebinars/")
        time.sleep(3)
        driver.get("http://127.0.0.1:8000/webinar/")
        time.sleep(3)
        driver.get("http://127.0.0.1:8000/org_profile/")
        aicte = driver.find_element(By.NAME, "aicte_id")
        aicte.clear()
        aicte.send_keys("1-36488387417")
        phone_number = driver.find_element(By.NAME, "phone_number")
        phone_number.clear()
        phone_number.send_keys("9034567890")

        website = driver.find_element(By.NAME, "website")
        website.clear()
        website.send_keys("https://www.model.in")

        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()
        time.sleep(5)
        driver.get("http://127.0.0.1:8000/login/")
        email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email.send_keys("ammu@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password.send_keys("Sample@123")
        time.sleep(2)
        submit = driver.find_element(By.CSS_SELECTOR, 'button#login.btn.btn-primary.btn-block.register-btn')
        submit.click()
        time.sleep(2)
        events = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/recommendations/"]')
        events.click()
        time.sleep(2)
        view = driver.find_element(By.CSS_SELECTOR, "a.btn[href='/view_webinar/68']")
        view.click()
        time.sleep(2)
        logout = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/logout/']")
        logout.click()
        time.sleep(2)
    # def test_01_login_page(self):
    #     driver = self.driver
    #     driver.get(self.live_server_url)
    #     driver.maximize_window()
    #     time.sleep(1)
    #     login = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/login/"]')
    #     login.click()
    #     time.sleep(2)
    #     email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    #     email.send_keys("elizatom9@gmail.com")
    #     password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    #     password.send_keys("Eliza@123")
    #     time.sleep(2)
    #     submit = driver.find_element(By.CSS_SELECTOR, 'button#login.btn.btn-primary.btn-block.register-btn')
    #     submit.click()
    #     time.sleep(2)
    #     events = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/recommendations/"]')
    #     events.click()
    #     time.sleep(2)
    #     view = driver.find_element(By.CSS_SELECTOR, "a.btn[href='/view_webinar/68']")
    #     view.click()
    #     time.sleep(2)
    #     logout = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/logout/']")
    #     logout.click()
    #     time.sleep(2)
    #     login = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/login/"]')
    #     login.click()
    #     time.sleep(2)
    #     email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    #     email.send_keys("elizebaththomas2024@mca.ajce.in")
    #     password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    #     password.send_keys("Eliza@123")
    #     time.sleep(2)
    #     submit = driver.find_element(By.CSS_SELECTOR, 'button#login.btn.btn-primary.btn-block.register-btn')
    #     submit.click()
    #     time.sleep(2)
    #     profile = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/org_profile/']")
    #     profile.click()
    #     time.sleep(2)
    #     logout = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/logout/']")
    #     logout.click()
    #     time.sleep(2)

if __name__ == '__main__':
    import unittest
    unittest.main()