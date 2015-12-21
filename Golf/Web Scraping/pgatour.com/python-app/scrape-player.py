# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import time
import csv
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

def lookup_career(player_id, filename, href):
    try:
        desired_capabilities = dict()
        desired_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        desired_capabilities['unexpectedAlertBehaviour'] = "ignore"
        driver = webdriver.Firefox(capabilities=desired_capabilities)

        # driver = webdriver.Chrome(os.path.dirname(os.path.abspath(__file__)) + r"\chromedriver.exe")

        driver.get(href)

        height = driver.find_elements_by_css_selector("ul.player-bio-data:nth-of-type(1)>li:nth-of-type(1)>p:nth-of-type(1)")[0].get_attribute('textContent')
        weight = driver.find_elements_by_css_selector("ul.player-bio-data:nth-of-type(1)>li:nth-of-type(1)>p:nth-of-type(2)")[0].get_attribute('textContent')
        birthday = driver.find_elements_by_css_selector("ul.player-bio-data:nth-of-type(1)>li:nth-of-type(1)>p:nth-of-type(3)")[0].get_attribute('textContent')
        turned_pro = driver.find_elements_by_css_selector("ul.player-bio-data:nth-of-type(2)>li:nth-of-type(1)>p:nth-of-type(1)")[0].get_attribute('textContent')
        birthplace = driver.find_elements_by_css_selector("ul.player-bio-data:nth-of-type(2)>li:nth-of-type(1)>p:nth-of-type(2)")[0].get_attribute('textContent')

    except Exception, exc:
        print("EXCEPTION:")
        print("     ", str(exc))
        print("")

def get_player_info(player_csv, tour, start_id, stop_id, filename):
    try:
        with open(player_csv, 'r') as f:
            reader = csv.reader(f)
            player_list = list(reader)

        for player_line in player_list:
            player_id = player_line[0]
            player_num = int(player_id[3:])
            player_tour = player_line[2]
            ptc_player_id = int(str(player_line[3]).split("/")[4].split('.')[1])
            ptc_player_name = int(str(player_line[3]).split("/")[4].split('.')[2])

            if player_tour==tour and player_id <= start_id <= stop_id:

                href_career="http://www.pgatour.com/players/player." + ptc_player_id + "." + ptc_player_name + ".html/career"
                lookup_career(player_id, filename, href_career)

    except Exception, exc:
        print("EXCEPTION:")
        print("     ", str(exc))
        print("")



if __name__ == '__main__':
