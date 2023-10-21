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
        email.send_keys("elizatom9@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password.send_keys("Eliza@123")
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
        login = driver.find_element(By.CSS_SELECTOR, 'a.nav-link[href="/login/"]')
        login.click()
        time.sleep(2)
        email = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
        email.send_keys("elizebaththomas2024@mca.ajce.in")
        password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password.send_keys("Eliza@123")
        time.sleep(2)
        submit = driver.find_element(By.CSS_SELECTOR, 'button#login.btn.btn-primary.btn-block.register-btn')
        submit.click()
        time.sleep(2)
        profile = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/org_profile/']")
        profile.click()
        time.sleep(2)
        logout = driver.find_element(By.CSS_SELECTOR, "a.nav-link[href='/logout/']")
        logout.click()
        time.sleep(2)

if __name__ == '__main__':
    import unittest
    unittest.main()