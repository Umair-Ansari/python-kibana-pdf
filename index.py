import logging
import math
import json
from flask import jsonify, abort, make_response
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pydf

from constants import Constants
from response import Response


class SeleniumCrawler(object):

    def get_page(self, url):
        response = Response()
        try:

            # Initilized the chrome driver
            print("Initilized the chrome driver")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--window-size=1420,1080')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')
            browser = webdriver.Chrome(chrome_options=chrome_options)

            # browser kibana
            print("browser kibana")
            browser.get(url)
            delay = 10000

            # wait till specific classes appears
            print("wait till specific classes appears")
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'kbn-table')))
            body = browser.find_element_by_class_name("kbn-table").get_attribute('innerHTML')

            # calculate number of pages exists and loop them
            print("calculate number of pages exists and loop them")
            pages = (str(browser.find_element_by_class_name("kuiToolBarText").text).split(" ")[2]).replace(",","")
            pages = math.ceil(int(pages) / 50) - 1

            print("pages found {}".format(pages))
            for page in range(1, pages):
                browser.execute_script("document.getElementsByClassName('kuiButton')[1].click()")
                chunk = browser.find_element_by_class_name("kbn-table").get_attribute('innerHTML').replace("<tbody>", "")
                body += chunk

            # apply table tags and generate pdf
            print("apply table tags and generate pdf")
            pdf = pydf.generate_pdf("<table>" + body + "</table>")
            with open('out.pdf', 'wb') as f:
                f.write(pdf)

            return json.loads(json.dumps((response.get_response(Constants.SUCCESS, Constants.SUCCESS))))
        except Exception as e:
            logging.exception(e)

            return abort(make_response(jsonify(response.get_response(Constants.SERVER_ERROR, Constants.SERVER_ERROR)), response.get_code(Constants.SERVER_ERROR)))

