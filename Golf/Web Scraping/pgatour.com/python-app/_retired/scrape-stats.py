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


project_directory = os.path.dirname(os.path.abspath(__file__))
data_filename = project_directory + r"\player-names.csv"

lookup(data_filename)

def write_output(filename, values):
    with codecs.open(filename, "a+", encoding='utf-8') as f:
        for c in range(0, len(values)):
            if c == 0:
                f.write('"' + unicode(values[c]).replace(u"\u00A0", " ") + '"')
            else:
                f.write(',"' + unicode(values[c]).replace(u"\u00A0", " ") + '"')
        f.write("\n")

def lookup(input_filename, player_output_file, tournament_output_file, id_start, id_stop):
    output_ids = list()

    player_stat_fields = 19
    tournament_stat_fields=6

    if os.path.isfile(player_output_file) is False:
        with codecs.open(player_output_file, "w+", encoding='utf-8') as f:
            f.write('"name_id","name","stats_href",' +
                    '"country","height","weight","date_of_birth","year_turned_pro","college","birthplace",' +
                    '"season_starts","season_first","season_second","season_third","season_top10","season_top25",' +
                    '"season_made_cut","season_cut","season_withdrew","season_money","season_fedex_points","season_fedex_rank"' +
                    '"lookup_date_time","lookup_status"\n')
    else:
        with codecs.open(player_output_file, "r", encoding='utf-8') as f:
            for line in f:
                output_ids.append(line.split(",")[0].strip('"'))
                
                
    with codecs.open(tournament_output_file, "w+", encoding='utf-8') as f:
        f.write('name_id')

    with codecs.open(input_filename, "r" encoding='utf-8') as f:
        for line in f:
            input_id=line.split(",")[0].strip('"')
            input_name=line.split(",")[1].strip('"')
            input_link=line.split(",")[2].strip('"')

            output_rec=list()

            output_rec.append(input_id)
            output_rec.append(input_name)
            output_rec.append(input_link)

            try:
                id_in_range = (id_start <= int(input_id) <= id_stop)
            except ValueError:
                id_in_range = False

            if input_id not in output_ids and id_in_range is True:

            failed_attempts = 0

            restart_browser = False

            while failed_attempts < 3:  # Loop 02
                if restart_browser == True:
                    try:
                        driver.quit()
                    except:
                        pass

                driver = webdriver.Chrome(os.path.dirname(os.path.abspath(__file__)) + r"\chromedriver.exe")

                try:
                    driver.get(input_link)
                    player_stats=list()
                    tournament_stats=list()
            
                    country=driver.find_element_by_css_selector(".title-head>.icon>img").get_attribute("alt")
            
                    height=driver.find_element_by_css_selector(".player-bio-data>.col1>p:nth-child(1)").get_attribute("textContent")
                    weight=driver.find_element_by_css_selector(".player-bio-data>.col1>p:nth-child(2)").get_attribute("textContent")
                    birthday=driver.find_element_by_css_selector(".player-bio-data>.col1>p:nth-child(3)").get_attribute("textContent")
                    college=driver.find_element_by_css_selector(".player-bio-data>.col2>p:nth-child(1)").get_attribute("textContent")
                    year_turned_pro=driver.find_element_by_css_selector(".player-bio-data>.col2>p:nth-child(2)").get_attribute("textContent")
                    birthplace=driver.find_element_by_css_selector(".player-bio-data>.col2>p:nth-child(3)").get_attribute("textContent")
            
                    driver.get(input_link + '/season')
            
                    season_starts=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(1)").get_attribute("textContent")
                    season_first=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(2)").get_attribute("textContent")
                    season_second=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(3)").get_attribute("textContent")
                    season_third=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(4)").get_attribute("textContent")
                    season_top10=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(5)").get_attribute("textContent")
                    season_top25=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(6)").get_attribute("textContent")
                    season_made_cut=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(7)").get_attribute("textContent")
                    season_cut=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(8)").get_attribute("textContent")
                    season_withdrew=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(9)").get_attribute("textContent")
                    season_money=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(10)").get_attribute("textContent")
                    season_fedex_points=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(11)").get_attribute("textContent")
                    season_fedex_rank=driver.find_element_by_css_selector(".players-career-table-row>td:nth-child(1)").get_attribute("textContent")


                    player_stats.append=[country,height,weight,birthday,year_turned_pro,college,birthplace]
                    player_stats=player_stats+[season_starts,season_first,season_second,season_third,
                                               season_top10,season_top25,season_made_cut,season_cut,
                                               season_withdrew,season_money,season_fedex_points,season_fedex_rank]

                    rows=driver.find_elements_by_css_selector(".player-season-results>.table-styled>tbody>tr")

                    row_count=0;
                    for row in rows:
                        row_count += 1
                        if row_count > 1:
                            t_date=row.find_element("td:nth-child(1)").get_attribute("textContent")
                            t_name=row.find_element("td:nth-child(2)").get_attribute("textContent")
                            t_pos=row.find_element("td:nth-child(3)").get_attribute("textContent")
                            t_score_round1=row.find_element("td:nth-child(4)").get_attribute("textContent")
                            t_score_round2=row.find_element("td:nth-child(5)").get_attribute("textContent")
                            t_score_round3=row.find_element("td:nth-child(6)").get_attribute("textContent")
                            t_score_round4=row.find_element("td:nth-child(7)").get_attribute("textContent")
                            t_score_round5=row.find_element("td:nth-child(8)").get_attribute("textContent")
                            t_total_score=row.find_element("td:nth-child(9)").get_attribute("textContent")
                            t_score_to_par=row.find_element("td:nth-child(10)").get_attribute("textContent")
                            t_fedexcup_rank=row.find_element("td:nth-child(11)").get_attribute("textContent")
                            t_fedexcup_points=row.find_element("td:nth-child(12)").get_attribute("textContent")







                except Exception, exc:
                    print("EXCEPTION:")
                    print("     ", str(exc))
                    print("")
                    failed_attempts += 1
                    restart_browser = True
                    if failed_attempts >= 3:
                        output_recf = list(output_rec)
                        for k in range(player_stat_fields):
                            output_recf.append("")
                        output_recf.append(time.strftime("%c"))
                        output_recf.append("Error: " + str(exc).strip("\n"))
                        write_output(player_output_file, output_recf)
                        break
                    else:
                        continue

def scrape_stats(xd,link,player_file,tournament_file):
    try:









    except:
        raise




