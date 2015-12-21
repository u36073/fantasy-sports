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


def lookup(filename, href, tour, mode):
    try:
        if mode == "w+":
            with codecs.open(filename, mode, encoding='utf-8') as f:
                f.write('"name_id","name","tour","stats_href","lookup_date_time"\n')

        desired_capabilities = dict()
        desired_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        desired_capabilities['unexpectedAlertBehaviour'] = "ignore"
        driver = webdriver.Firefox(capabilities=desired_capabilities)

        # driver = webdriver.Chrome(os.path.dirname(os.path.abspath(__file__)) + r"\chromedriver.exe")

        driver.get(href)

        names = driver.find_elements_by_css_selector(".name>a")

        _name_id = 0

        for name in names:
            _name_id += 1
            output_rec = list()
            output_rec.append(tour[:3] + str(_name_id))
            output_rec.append(tour)

            _name = name.get_attribute('textContent')

            output_rec.append(_name)

            _link = name.get_attribute("href")
            output_rec.append(_link)

            output_rec.append(time.strftime("%c"))

            write_output(filename, output_rec)

        driver.close()

    except Exception, exc:
        print("EXCEPTION:")
        print("     ", str(exc))
        print("")


if __name__ == '__main__':
    project_directory = os.path.dirname(os.path.abspath(__file__))
    output_filename = project_directory + r"\data-output\player-names.csv"

    lookup(output_filename, "http://www.pgatour.com/players.html", "PGA", "w+")
    lookup(output_filename, "http://www.pgatour.com/champions/players.html", "CHAMPIONS", "a+")
    lookup(output_filename, "http://www.pgatour.com/webcom/players.html", "WEBCOM", "a+")
    lookup(output_filename, "http://www.pgatour.com/canada/en_us/players.html", "CANADA", "a+")
    lookup(output_filename, "http://www.pgatour.com/la/es/players.html", "LATINO", "a+")

