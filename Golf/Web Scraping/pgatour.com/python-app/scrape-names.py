# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import time
import codecs

import xlrd
from selenium import webdriver

# Import My Code Modules
import webautomation.general as wa_general
import webautomation.excel as wa_excel


def write_output(filename, values):
    with codecs.open(filename, "a+", encoding='utf-8') as f:
        for c in range(0, len(values)):
            if c == 0:
                f.write('"' + unicode(values[c]).replace(u"\u00A0", " ") + '"')
            else:
                f.write(',"' + unicode(values[c]).replace(u"\u00A0", " ") + '"')
        f.write("\n")


def lookup(filename):
    try:
        with codecs.open(filename, "w+", encoding='utf-8') as f:
            f.write('"name_id","name","stats_href","lookup_date_time"\n')

        # desired_capabilities = dict()
        # desired_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        # desired_capabilities['unexpectedAlertBehaviour'] = "ignore"
        # driver = webdriver.Firefox(capabilities=desired_capabilities)

        driver = webdriver.Chrome(os.path.dirname(os.path.abspath(__file__)) + r"\chromedriver.exe")

        driver.get("http://www.pgatour.com/players.html")

        names = driver.find_elements_by_css_selector(".name>a")

        _name_id = 0

        for name in names:
            _name_id += 1
            output_rec = list()
            output_rec.append(_name_id)

            _name = name.get_attribute('textContent')

            output_rec.append(_name)

            _link = name.get_attribute("href")
            output_rec.append(_link)

            output_rec.append(time.strftime("%c"))

            write_output(filename, output_rec)

    except Exception, exc:
        print("EXCEPTION:")
        print("     ", str(exc))
        print("")


project_directory = os.path.dirname(os.path.abspath(__file__))
output_filename = project_directory + r"\player-names.csv"

lookup(output_filename)
