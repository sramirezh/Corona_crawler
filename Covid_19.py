#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:58:45 2020
Web scrapping following https://towardsdatascience.com/how-to-track-coronavirus-with-python-a5320b778c8e


To enable cromedriver
https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de


TO solve problems with chrome driver
https://github.com/SeleniumHQ/selenium/issues/7132


The webtable class was taken from 

https://chercher.tech/python/table-selenium-python

@author: simon
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from tqdm import tqdm
from joblib import Parallel, delayed
import pandas as pd
import multiprocessing




class Coronavirus():
  def __init__(self):
    self.driver = webdriver.Chrome(options = chrome_options)
    self.driver.get('https://www.worldometers.info/coronavirus/')

# To run it headless
chrome_options = Options()  
chrome_options.add_argument("--headless")  


    

bot = Coronavirus()

table = bot.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]') # There are 2 table bodies
header = bot.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/thead')

#country_element = table.find_element_by_xpath("//tr[contains(text(), 'USA')]")
    
class WebTable:
    def __init__(self, webtable, data_type = "d"):
        """
        The type is d = data or h for header
        """
        self.type = data_type
        self.table = webtable
        self.row_number = self.get_row_count()
        self.column_number =  self.get_column_count()

    def get_row_count(self):
      return len(self.table.find_elements_by_tag_name("tr"))

    def get_column_count(self):
        if self.type == 'h':
            return int(len(self.table.find_elements_by_xpath("//tr/t%s"%self.type))/2)
        
        if self.type == 'd':
            return int(len(self.table.find_elements_by_xpath("//tr[1]/t%s"%self.type))/2) 

    def get_table_size(self):
        return {"rows": self.row_number,
                "columns": self.column_number}

    def row_data(self, row_number):
        """
        Important in HTML apparently the count starts in 1 not in 0
        """
        row_number = row_number
        row = self.table.find_elements_by_xpath("//tr["+str(row_number)+"]/t%s"%self.type)
        rData = []
        for webElement in row :
            rData.append(webElement.text)

        return rData

    def column_data(self, column_number):
        col = self.table.find_elements_by_xpath("//tr/t%s["%self.type+str(column_number)+"]")
        rData = []
        for webElement in col :
            rData.append(webElement.text)
        return rData

    def get_all_data(self):
        # get number of rows
        allData = []
        # iterate over the rows, to ignore the headers we have started the i with '1'
#        num_cores = multiprocessing.cpu_count()
#        allData = Parallel(n_jobs = num_cores)(delayed(self.row_data)(i+1) for i in tqdm(self.row_number))    
        for i in tqdm(range(self.row_number)):
            # reset the row data every time
            row = self.row_data(i+1)
            allData.append(row)
            
        return allData


#"""
#Using selenium methods
#"""  
#w = WebTable(table,"d")
#h = WebTable(header,"h")
#
#print("No of rows : ", w.get_row_count())
#print("------------------------------------")
#print("No of cols : ", w.get_column_count())
#print("------------------------------------")
#print("Table size : ", w.get_table_size())
#data = w.get_all_data()
#header = h.get_all_data()
        
    
    
"""
Using the patterns in the text
"""

rows = table.text.split('\n') #Need to be splitted in a smart way
h = header.text.split(' ')


get rows