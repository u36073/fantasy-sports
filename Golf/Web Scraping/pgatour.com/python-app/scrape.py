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


# id_start=465
# id_stop=525
# 
# project_directory=os.path.dirname(os.path.abspath(__file__))
# input_filename=project_directory + r"\zurich-input-phase2.xlsx"
# output_filename=project_directory + r"\zurich-output-phase2-" + str(id_start) + "-" + str(id_stop) + ".csv"

def write_output(filename, values):
    with codecs.open(filename, "a+", encoding='utf-8') as f:
        for c in range(0, len(values)):
            if c == 0:
                f.write('"' + unicode(values[c]) + '"')
            else:
                f.write(',"' + unicode(values[c]) + '"')
        f.write("\n")


def lookup(input_filename, output_filename, id_start, id_stop):
    output_ids = list()
    if os.path.isfile(output_filename) is False:
        with codecs.open(output_filename, "w+", encoding='utf-8') as f:
            f.write('"profile","gender","age","marital_status","model_spec","yr_vehicle",' +
                    '"postal_code","isBaseCase","var_1","var_2",' +
                    '"santan_province","santan_codigo_postal","santan_make","santan_model",' +
                    '"rd_fecha","rd_provincia","rd_localidad","rd_marca","rd_ano_de_fabricacion",' +
                    '"rd_modelo","rd_gnc","rd_suma_gnc","rd_fecha_de_nacimiento","rd_sexo",' +
                    '"rd_estado_civil","qt_compania","qt_plan","qt_cuota_mensual",' +
                    '"qt_suma_asegurada","qt_inspeccion","lookup_date_time","lookup_status"\n')
    else:
        with codecs.open(output_filename, "r", encoding='utf-8') as f:
            for line in f:
                output_ids.append(line.split(",")[0].strip('"'))
    # OutputFile.seek(0,0) # Set current postion of pointer to the beginning of the file.                
    inputwb = xlrd.open_workbook(input_filename)
    inputws = inputwb.sheet_by_name('input-data')

    restart_browser = True

    for row_index in range(1, inputws.nrows):  # Loop 01
        input_id = wa_excel.excel_to_string(inputws, row_index, 0)
        input_gender = wa_excel.excel_to_string(inputws, row_index, 1)
        input_age = wa_excel.excel_to_string(inputws, row_index, 2)
        input_marital_status = wa_excel.excel_to_string(inputws, row_index, 3)
        input_model_spec = wa_excel.excel_to_string(inputws, row_index, 4)
        input_year = wa_excel.excel_to_string(inputws, row_index, 5)
        input_postal_code = wa_excel.excel_to_string(inputws, row_index, 6)
        input_isbasecase = wa_excel.excel_to_string(inputws, row_index, 7)
        input_var1 = wa_excel.excel_to_string(inputws, row_index, 8)
        input_var2 = wa_excel.excel_to_string(inputws, row_index, 9)
        input_province = wa_excel.excel_to_string(inputws, row_index, 10)
        input_codigo_postal = wa_excel.excel_to_string(inputws, row_index, 11)
        input_make = wa_excel.excel_to_string(inputws, row_index, 12)
        input_model = wa_excel.excel_to_string(inputws, row_index, 13)

        output_rec = list()
        for k in range(0, 14):
            output_rec.append(wa_excel.excel_to_string(inputws, row_index, k))

        try:
            id_in_range = (int(input_id) >= id_start and int(input_id) <= id_stop)
        except ValueError:
            id_in_range = False

        if input_id not in output_ids and id_in_range is True:
            if input_model == '':
                output_recf = list(output_rec)
                for k in range(16):
                    output_recf.append("")
                output_recf.append(time.strftime("%c"))
                output_recf.append("Year/Make/Model Not Available")
                write_output(output_filename, output_recf)
                continue

            failed_attempts = 0
            while failed_attempts < 3:  # Loop 02
                restart_browser = True
                if restart_browser == True:
                    try:
                        driver.quit()
                    except:
                        pass

                    desired_capabilities = dict()
                    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
                    desired_capabilities['unexpectedAlertBehaviour'] = "ignore"
                    driver = webdriver.Firefox(capabilities=desired_capabilities)
                    try:
                        driver.get("http://www.santanderrioseguros.com.ar/portal/cotizador.jsp?cdRamo=40")
                        restart_browser = True
                    except:
                        restart_browser = True
                        continue
                try:
                    wa_general.link_click(driver, "#button_cdProvCmb")

                    provinces = list()
                    provinces = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(8) a")
                    for province in provinces:
                        if province.text == input_province:
                            province.click()
                            break
                    time.sleep(1)

                    # #_cdCiudadCmb
                    # ul.ui-autocomplete:nth-child(9) > li:nth-child(1) > a:nth-child(1)

                    e = driver.find_element_by_css_selector("#_cdCiudadCmb")
                    e.click()
                    e.send_keys(input_codigo_postal)
                    time.sleep(1)

                    postal_codes = list()
                    postal_codes = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(9) a")
                    for postal_code in postal_codes:
                        if postal_code.text == input_codigo_postal:
                            postal_code.click()
                            break
                    time.sleep(1)

                    wa_general.type_text(driver, input_year, "#anio")

                    wa_general.link_click(driver, "#_cdMarcaCmb")
                    time.sleep(1)
                    wa_general.type_text(driver, input_make, "#_cdMarcaCmb")
                    time.sleep(1)
                    makes = list()
                    makes = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(11) a")
                    for make in makes:
                        if make.text == input_make:
                            make.click()
                            break
                    time.sleep(1)

                    #################################################################################
                    # Vehicle Model Entry
                    #################################################################################
                    list_found = False
                    xmodel = input_model.split('$')[0]
                    xmodel_len = len(xmodel)
                    input_len = xmodel_len
                    tries = 0
                    while tries < 4:
                        tries += 1
                        if tries == 2:
                            input_len = int(xmodel_len / 2)
                        if tries == 3:
                            input_len = int(xmodel_len / 4)
                        if tries == 4:
                            input_len = 1
                        wa_general.link_click(driver, "#_cdModeloCmb")
                        wa_general.type_text(driver, xmodel[:input_len], "#_cdModeloCmb")
                        time.sleep(1)
                        models = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(12) a")
                        if len(models) > 0:
                            list_found = True
                            flag = False
                            for model in models:
                                # print(model.text)
                                # print(str(model.text).split('$')[0])
                                # print(input_model)
                                # print(input_model.split('$')[0])
                                # print("------------------------------------------------------------------------")
                                if str(model.text).split('$')[0] == input_model.split('$')[0]:
                                    flag = True
                                    model.click()
                                    break
                            if flag is False and tries >= 4:
                                failed_attempts = 3
                                raise Exception("Vehicle model not found (1)")
                            elif flag is False and tries < 4:
                                continue
                            else:
                                time.sleep(1)
                                break
                        else:
                            continue
                    if list_found is False:
                        failed_attempts = 3
                        raise Exception("Vehicle model not found (2)")
                    time.sleep(1)
                    ###################################################################################

                    wa_general.link_click(driver, "#button_inSexoCmb")
                    time.sleep(1)
                    options = list()
                    options = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(15) a")
                    if input_gender.upper() == "MALE":
                        gender = "MASCULINO"
                    else:
                        gender = "FEMENINO"

                    for option in options:
                        if option.text == gender:
                            option.click()
                            break
                    time.sleep(1)

                    wa_general.link_click(driver, "#button_cdEdoCivilCmb")
                    time.sleep(1)
                    options = list()
                    options = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(16) a")

                    if input_marital_status.upper() == "MARRIED":
                        marital_status = "CASADO/A"
                    elif input_marital_status.upper() == "DIVORCED":
                        marital_status = "DIVORCIADO/A"
                    elif input_marital_status.upper() == "WIDOWED":
                        marital_status = "VIUDO/A"
                    else:
                        marital_status = "SOLTERO/A"

                    for option in options:
                        if option.text == marital_status:
                            option.click()
                            break
                    time.sleep(1)

                    pinfo = wa_argentina.get_identifying_info(input_gender, int(input_age))

                    wa_general.link_click(driver, ".ui-datepicker-trigger")
                    time.sleep(1)

                    wa_general.list_select_text(driver, pinfo['birth_month_abbr'], ".ui-datepicker-month")
                    wa_general.list_select_text(driver, pinfo['birth_year'], ".ui-datepicker-year")

                    e = driver.find_element_by_xpath("/html/body/div[2]/table/tbody//a[.='" + pinfo['birth_day'] + "']")
                    e.click()

                    wa_general.link_click(driver, "#button_cdRamoCmb")
                    time.sleep(1)
                    options = list()
                    options = driver.find_elements_by_css_selector("ul.ui-autocomplete:nth-child(14) a")
                    for option in options:
                        if unicode(option.text) == u"TODAS LAS COMPAÑIAS":
                            option.click()
                            break
                    time.sleep(1)
                    wa_general.link_click(driver, "#botonCotizar")

                    wa_general.wait_for(driver,
                                        ".table_none > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(14) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)",
                                        30)

                    messages = driver.find_elements_by_css_selector(
                        "#formCotizaciones > table:nth-child(21) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > table:nth-child(2) > tbody:nth-child(1) > tr:nth-child(1) > th:nth-child(1)")

                    if len(messages) > 0:
                        for message in messages:
                            msg_text = message.text
                            if msg_text.upper().strip() == "AVISO":
                                failed_attempts = 3
                                raise Exception("No quotes available for this vehicle.")

                    e = driver.find_element_by_css_selector(
                        ".table_none > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > table:nth-child(14) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)")

                    output_recfa = list()
                    output_recfa = list(output_rec)

                    fields = e.text
                    for field in fields.split("\n"):
                        output_recfa.append(field)

                    # table-viewCTx > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2) > img:nth-child(1)

                    flag = False
                    for row in range(1, 999):
                        try:
                            output_recfb = list()
                            output_recfb = list(output_recfa)
                            cell = driver.find_element_by_css_selector(
                                "#table-viewCTx > tbody:nth-child(2) > tr:nth-child(" + str(
                                    row) + ") > td:nth-child(2) > img:nth-child(1)")
                            output_recfb.append(cell.get_attribute("title"))
                            flag = True
                            cell = driver.find_element_by_css_selector(
                                "#table-viewCTx > tbody:nth-child(2) > tr:nth-child(" + str(
                                    row) + ") > td:nth-child(3)")
                            output_recfb.append(cell.text)
                            cell = driver.find_element_by_css_selector(
                                "#table-viewCTx > tbody:nth-child(2) > tr:nth-child(" + str(
                                    row) + ") > td:nth-child(4)")
                            output_recfb.append(cell.text)
                            cell = driver.find_element_by_css_selector(
                                "#table-viewCTx > tbody:nth-child(2) > tr:nth-child(" + str(
                                    row) + ") > td:nth-child(5)")
                            output_recfb.append(cell.text)
                            cell = driver.find_element_by_css_selector(
                                "#table-viewCTx > tbody:nth-child(2) > tr:nth-child(" + str(
                                    row) + ") > td:nth-child(8)")
                            output_recfb.append(cell.text)
                            output_recfb.append(time.strftime("%c"))
                            output_recfb.append("Success")
                            write_output(output_filename, output_recfb)
                        except:
                            if flag is False:
                                raise Exception("No quotes returned or error in the quote page returned.")
                            else:
                                break
                    break
                except Exception, exc:
                    print("EXCEPTION:")
                    print("     ", str(exc))
                    print("")
                    failed_attempts += 1
                    restart_browser = True
                    if failed_attempts >= 3:
                        output_recf = list(output_rec)
                        for k in range(16):
                            output_recf.append("")
                        output_recf.append(time.strftime("%c"))
                        output_recf.append("Error: " + str(exc).strip("\n"))
                        write_output(output_filename, output_recf)
                        break
                    else:
                        continue
                        # End: Loop 02
                        # End: If 01
                        # End: Loop 01
