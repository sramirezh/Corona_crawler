#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 20:18:52 2019
Following https://dzone.com/articles/make-python-surf-the-web-for-you-and-send-best-fli
In mac install chromdedriver with homebrew: brew cask install chromedriver
@author: simon
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import pandas as pd

import time
import datetime

# To send emails
import smtplib
from email.mime.multipart import MIMEMultipart


browser = webdriver.Chrome(executable_path='chromedriver')

#Setting ticket types paths
return_ticket = "//label[@id='flight-type-roundtrip-label-hp-flight']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

def ticket_chooser(ticket):
    try:
        ticket_type = browser.find_element_by_xpath(ticket)
        ticket_type.click()
    except Exception as e:
        pass
    
"""
The general idea for the next functions is: 
    -to get the id of the field, inspecting the website.
    -clearing the field
    -filling it with send_keys
"""

def dep_country_chooser(dep_country):
    fly_from = browser.find_element_by_xpath("//input[@id='flight-origin-hp-flight']")
    time.sleep(1)
    fly_from.clear()
    time.sleep(1.5)
    fly_from.send_keys('  ' + dep_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()
    
    

def arrival_country_chooser(arrival_country):
    """
    time.sleep is required to give time for the website to look for information
    """
    fly_to = browser.find_element_by_xpath("//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(1.5)
    first_item = browser.find_element_by_xpath("//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()
    
    

def dep_date_chooser(month, day, year):
    dep_date_button = browser.find_element_by_xpath("//input[@id='flight-departing-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys(month + '/' + day + '/' + year)
    
    
    
def return_date_chooser(month, day, year):
    
    """
    For the return date, clearing whatever was written wasn't working for some reason (probably due to 
    the page having this as autofill not allowing me to override it with .clear())

    The way I worked around this is by using Keys.BACKSPACE which simply tells Python to 
    click backspace (to delete whatever is written in the date field). I put it in a for loop
    to click backspace 11 times to delete all the characters for the date in the field.
    """
    
    return_date_button = browser.find_element_by_xpath("//input[@id='flight-returning-hp-flight']")
    for i in range(11):
        return_date_button.send_keys(Keys.BACKSPACE)
    return_date_button.send_keys(month + '/' + day + '/' + year)
    
    
def search():
    search = browser.find_element_by_xpath("//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    time.sleep(15)
    print('Results ready!')
    
    

df = pd.DataFrame()
def compile_data():
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list
    #departure times
    dep_times = browser.find_elements_by_xpath("//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]
    #arrival times
    arr_times = browser.find_elements_by_xpath("//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]
    #airline name
    airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]
    #prices
    prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text.split("$")[1] for value in prices]
    #durations
    durations = browser.find_elements_by_xpath("//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]
    #stops
    stops = browser.find_elements_by_xpath("//span[@class='number-stops']")
    stops_list = [value.text for value in stops]
    #layovers
    layovers = browser.find_elements_by_xpath("//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]
    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass
    print('Excel Sheet Created!')
    
    
    
link = 'https://www.expedia.com/'
browser.get(link)
time.sleep(5)
#choose flights only
flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
flights_only.click()
ticket_chooser(return_ticket)
dep_country_chooser('Cairo')
arrival_country_chooser('New york')
dep_date_chooser('04', '01', '2019')
return_date_chooser('05', '02', '2019')
search()
compile_data()
    
#for i in range(8):    
#    link = 'https://www.expedia.com/'
#    browser.get(link)
#    time.sleep(5)
#    #choose flights only
#    flights_only = browser.find_element_by_xpath("//button[@id='tab-flight-tab-hp']")
#    flights_only.click()
#    ticket_chooser(return_ticket)
#    dep_country_chooser('Cairo')
#    arrival_country_chooser('New york')
#    dep_date_chooser('04', '01', '2019')
#    return_date_chooser('05', '02', '2019')
#    search()
#    compile_data()
#    #save values for email
#    current_values = df.iloc[0]
#    cheapest_dep_time = current_values[0]
#    cheapest_arrival_time = current_values[1]
#    cheapest_airline = current_values[2]
#    cheapest_duration = current_values[3]
#    cheapest_stops = current_values[4]
#    cheapest_price = current_values[-1]
#    print('run {} completed!'.format(i))
#    create_msg()
#    connect_mail(username,password)
#    send_email(msg)
#    print('Email sent!')
#    df.to_excel('flights.xlsx')
#    time.sleep(3600)