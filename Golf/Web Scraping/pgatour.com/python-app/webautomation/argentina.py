# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import random
from datetime import timedelta
from datetime import date

from pympler import tracker
import xlrd

from webautomation import excel


__excel_file__ = os.path.dirname(os.path.abspath(__file__)) + r"\personal-info-seed-lists.xlsx"
__first_names_male__ = list()
__first_names_female__ = list()
__last_names__ = list()
__email_suffixes__ = list()
__min_id__ = dict()
__max_id__ = dict()


def __import_data__():
    wb = xlrd.open_workbook(__excel_file__)

    ws = wb.sheet_by_name("male-first-names")
    for row_index in range(ws.nrows):
        x = excel.excel_to_string(ws, row_index, 0)
        if x <> "": __first_names_male__.append(x)
    #         print(x,"-",isinstance(__first_names_male__[len(__first_names_male__)-1], unicode))

    ws = wb.sheet_by_name("female-first-names")
    for row_index in range(ws.nrows):
        x = excel.excel_to_string(ws, row_index, 0)
        if x <> "": __first_names_female__.append(x)

    ws = wb.sheet_by_name("last-names")
    for row_index in range(ws.nrows):
        x = excel.excel_to_string(ws, row_index, 0)
        if x <> "": __last_names__.append(x)

    ws = wb.sheet_by_name("email-suffixes")
    for row_index in range(ws.nrows):
        x = excel.excel_to_string(ws, row_index, 0)
        if x <> "": __email_suffixes__.append(x)

    ws = wb.sheet_by_name("national-id")
    for row_index in range(1, ws.nrows - 1):
        year = excel.excel_to_string(ws, row_index, 0)
        minid = excel.excel_to_string(ws, row_index, 1)
        maxid = excel.excel_to_string(ws, row_index, 2)
        if year <> "" and minid <> "" and maxid <> "":
            __min_id__[year] = minid
            __max_id__[year] = maxid

__import_data__()


def get_identifying_info(gender, age):
    g = str(gender).upper()
    ident = dict()

    tabin = u"áéíóúüñÑÉ"
    tabout = u"aeiouunNE"
    tabin = [ord(char) for char in tabin]
    translate_table = dict(zip(tabin, tabout))

    ident['last_name'] = str(unicode(random.choice(__last_names__)).translate(translate_table))

    if g == "F" or g == "FEMALE":
        ident['first_name'] = str(unicode(random.choice(__first_names_female__)).translate(translate_table))
    else:
        ident['first_name'] = str(unicode(random.choice(__first_names_male__)).translate(translate_table))

    ident['email'] = ident["first_name"] + "." + ident["last_name"] + "@" + random.choice(__email_suffixes__)

    birthdate = date.today() - timedelta(days=age * 365 + random.choice(range(1, 365 - age)))

    ident['birth_year'] = str(birthdate.year)
    ident['birth_month'] = str(birthdate.month)
    ident['birth_monthz'] = "{:0>2d}".format(birthdate.month)

    if birthdate.month == 1:
        ident['birth_month_abbr'] = "Ene"
    elif birthdate.month == 2:
        ident['birth_month_abbr'] = "Feb"
    elif birthdate.month == 3:
        ident['birth_month_abbr'] = "Mar"
    elif birthdate.month == 4:
        ident['birth_month_abbr'] = "Abr"
    elif birthdate.month == 5:
        ident['birth_month_abbr'] = "May"
    elif birthdate.month == 6:
        ident['birth_month_abbr'] = "Jun"
    elif birthdate.month == 7:
        ident['birth_month_abbr'] = "Jul"
    elif birthdate.month == 8:
        ident['birth_month_abbr'] = "Ago"
    elif birthdate.month == 9:
        ident['birth_month_abbr'] = "Set"
    elif birthdate.month == 10:
        ident['birth_month_abbr'] = "Oct"
    elif birthdate.month == 11:
        ident['birth_month_abbr'] = "Nov"
    elif birthdate.month == 12:
        ident['birth_month_abbr'] = "Dic"

    ident['birth_day'] = str(birthdate.day)
    ident['birth_dayz'] = "{:0>2d}".format(birthdate.day)
    ident['birth_datez'] = ident['birth_dayz'] + "/" + ident['birth_monthz'] + "/" + ident['birth_year']

    minid = int(__min_id__[str(birthdate.year)])
    maxid = int(__max_id__[str(birthdate.year)])
    ident['national_id'] = str("{:0>8d}".format(random.choice(range(minid, maxid))))

    ident['area_code'] = str('11')
    ident['phone_number'] = '{:0>8d}'.format(random.randint(10000000, 99999999))

    return ident

# for x in range(0,1000):
#     pinfo=get_identifying_info("F",45)    
#     print(pinfo)
    
    
    



    
    
    
    