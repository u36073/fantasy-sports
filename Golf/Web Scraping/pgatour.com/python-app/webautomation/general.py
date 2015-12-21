# -*- coding: utf-8 -*-
from __future__ import print_function
import time
from selenium.webdriver.common.by import By as swdBy
from selenium.webdriver.support.wait import WebDriverWait as swdWait
from selenium.webdriver.support import expected_conditions as swdExpCond
from selenium.webdriver.support import select as swdSelect


def wait_for(wd, css, wait=20):
    try:
        swdWait(wd, wait).until(swdExpCond.element_to_be_clickable((swdBy.CSS_SELECTOR, css)),
                                "wait_for --> Element not found or not clickable: " + css)
        return None
    except:
        raise


def wait_for_list_box_items(wd, css, min_items=1, wait=15):
    wait_flag = True
    iterations = 1
    while wait_flag == True:
        options = wd.find_elements_by_css_selector(css + " > option:nth-child(" + str(min_items) + ")")
        if len(options) > 0:
            wait_flag = False
        else:
            time.sleep(1)
            iterations += 1
            if iterations > wait:
                wait_flag = False


def check_and_accept_popup_alert(wd, wait=1):
    try:
        swdWait(wd, wait).until(swdExpCond.alert_is_present(), "Popup Alert Window Not Found")
        popup = wd.switch_to_alert()
        message = popup.text
        popup.accept()
        return message
    except:
        return "_NOALERT_"


def get_selected_text(wd, css, wait=20):
    try:
        e = swdWait(wd, wait).until(swdExpCond.element_to_be_clickable((swdBy.CSS_SELECTOR, css)),
                                    "get_select_text --> Element not found or not clickable: " + css)
        return swdSelect.Select(e).first_selected_option.text
    except:
        raise


def list_select_text(wd, text, css, wait=20):
    try:
        e = swdWait(wd, wait).until(swdExpCond.element_to_be_clickable((swdBy.CSS_SELECTOR, css)),
                                    "list_select_text --> Element not found or not clickable: " + css)
        swdSelect.Select(e).select_by_visible_text(text)
        return None
    except:
        raise


def type_text(wd, text, css, wait=20):
    try:
        e = swdWait(wd, wait).until(swdExpCond.element_to_be_clickable((swdBy.CSS_SELECTOR, css)),
                                    "type_text --> Element not found or not clickable: " + css)
        e.clear()
        time.sleep(.5)
        e.send_keys(text)
        return None
    except:
        raise


def option_select(wd, css, wait=20):
    try:
        e = swdWait(wd, wait).until(swdExpCond.element_to_be_clickable((swdBy.CSS_SELECTOR, css)),
                                    "option_select --> Element not found or not clickable: " + css)
        e.click()
        return None
    except:
        raise


def link_click(wd, css, wait=20, pause_before_click=0):
    try:
        e = swdWait(wd, wait).until(swdExpCond.element_to_be_clickable((swdBy.CSS_SELECTOR, css)),
                                    "link_click --> Element not found or not clickable: " + css)
        time.sleep(pause_before_click)
        e.click()
        return None
    except:
        raise
