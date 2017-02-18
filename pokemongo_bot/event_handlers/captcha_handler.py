from __future__ import print_function
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import requests

from pokemongo_bot.event_manager import EventHandler

class CaptchaHandler(EventHandler):
	def __init__(self, bot):
		super(CaptchaHandler, self).__init__()
		self.bot = bot

	def handle_event(self, event, sender, level, formatted_msg, data):
		if event in ('pokestop_searching_too_often', 'login_successful'):
			self.bot.logger.info('Checking for captcha challenge.')

			response_dict = self.bot.api.check_challenge()
			challenge = response_dict['responses']['CHECK_CHALLENGE']
			print(challenge)
			if not challenge.get('show_challenge'):
				return
			url = challenge['challenge_url']
			try:
				chrome_options = Options()
				chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
				driver = webdriver.Chrome(chrome_options=chrome_options)
				driver.set_window_size(600, 600)
			except Exception as ex:
				print(ex)
				return

			driver.get(url)
			print(url)

			elem = driver.find_element_by_class_name("g-recaptcha")
			driver.execute_script("arguments[0].scrollIntoView(true);", elem)
			# Waits 1 minute for you to input captcha
			try:
				WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element_value((By.NAME, "g-recaptcha-response"), ""))
				print("Solved captcha")
				token = driver.execute_script("return grecaptcha.getResponse()")
				driver.quit()
				print("Recaptcha token: {}".format(token))
				response = self.bot.api.verify_challenge(token = token)
				print("Response:{}".format(response))
				time.sleep(1)
			except TimeoutException, err:
				print("Timed out while manually solving captcha")