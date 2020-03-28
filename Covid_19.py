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


class Coronavirus():
  def __init__(self):
    self.driver = webdriver.Chrome()
    self.driver.get('https://www.worldometers.info/coronavirus/')
    
    
bot = Coronavirus()

table = bot.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')

#country_element = table.find_element_by_xpath("//tr[contains(text(), 'USA')]")
    
class WebTable:
    def __init__(self, webtable):
       self.table = webtable
       self.row_number = self.row_count()
       self.column_number =  self.column_count()

    def get_row_count(self):
      return len(self.table.find_elements_by_tag_name("tr")) - 1

    def get_column_count(self):
        return int(len(self.table.find_elements_by_xpath("//tr[2]/td"))/2)

    def get_table_size(self):
        return {"rows": self.row_number,
                "columns": self.column_number}

    def row_data(self, row_number):
        if(row_number == 0):
            raise Exception("Row number starts from 1")

        row_number = row_number + 1
        row = self.table.find_elements_by_xpath("//tr["+str(row_number)+"]/td")
        rData = []
        for webElement in row :
            rData.append(webElement.text)

        return rData

    def column_data(self, column_number):
        col = self.table.find_elements_by_xpath("//tr/td["+str(column_number)+"]")
        rData = []
        for webElement in col :
            rData.append(webElement.text)
        return rData

    def get_all_data(self):
        # get number of rows
        noOfRows = len(self.table.find_elements_by_xpath("//tr")) -1
        # get number of columns
        noOfColumns = int(len(self.table.find_elements_by_xpath("//tr[2]/td"))/2)
        allData = []
        # iterate over the rows, to ignore the headers we have started the i with '1'
        for i in range(2, noOfRows):
            # reset the row data every time
            ro = []
            # iterate over columns
            for j in range(1, noOfColumns) :
                # get text from the i th row and j th column
                ro.append(self.table.find_element_by_xpath("//tr["+str(i)+"]/td["+str(j)+"]").text)

            # add the row data to allData of the self.table
            allData.append(ro)

        return allData

    def presence_of_data(self, data):

        # verify the data by getting the size of the element matches based on the text/data passed
        dataSize = len(self.table.find_elements_by_xpath("//td[normalize-space(text())='"+data+"']"))
        presence = false
        if(dataSize > 0):
            presence = true
        return presence

    def get_cell_data(self, row_number, column_number):
        if(rowNumber == 0):
            raise Exception("Row number starts from 1")

        rowNumber = rowNumber+1
        cellData = table.find_element_by_xpath("//tr["+str(row_number)+"]/td["+str(column_number)+"]").text
        return cellData
    
    
    
w = WebTable(table)
print("No of rows : ", w.get_row_count())
print("------------------------------------")
print("No of cols : ", w.get_column_count())
print("------------------------------------")
print("Table size : ", w.get_table_size())
print("------------------------------------")
print("First row data : ", w.row_data(1))
print("------------------------------------")
print("First column data : ", w.column_data(1))
print("------------------------------------")
print("All table data : ", w.get_all_data())
print("------------------------------------")
print("presence of data : ", w.presence_of_data("Chercher.tech"))
print("------------------------------------")
print("Get data from Cell : ", w.get_cell_data(2, 2))