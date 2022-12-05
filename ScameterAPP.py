#20221204 - First attempt using streamlit
#Ref: https://towardsdatascience.com/getting-started-with-streamlit-web-based-applications-626095135cb8

#import required library
import streamlit as st
import os, sys

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta
import math
import requests
import numpy as np
import re


#required function
def scameterCheck(frame):
    if isinstance(frame, pd.DataFrame):
        #Input the weblink
        link = "https://cyberdefender.hk/en-us/"
        
        #Create instance of chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(0.5)
        
        for i in range(frame.count()[0]):
            value = frame['Value'].iloc[i]
            #Open the link
            driver.get(link)
            time.sleep(3)
            
            #Clear the value of search bar and input new value
            driver.find_element_by_id('search').clear()
            driver.find_element_by_id('search').send_keys(value)

            #Click the submit button
            driver.find_element_by_xpath('//*[@id="post-3646"]/div/div/section[2]/div/div/div/div/div/form/div/div/div[1]/div[2]/div[2]').click()
            time.sleep(5)

            Result = driver.find_element_by_xpath('/html/body/form/section/div[2]/div[1]/div[2]/h1').text
            risk = driver.find_element_by_xpath('/html/body/form/section/div[2]/div[1]/div[1]/img').get_attribute("src").rsplit('/', 1)[-1]
            RiskRating = re.sub("_en.webp", "", risk)
            
            frame['Result'].iloc[i] = Result
            frame['RiskRating'].iloc[i] = RiskRating
    else: print("input not dataframe")


# Add a title and intro text
st.title('Bulk checking on Scameter')
st.text('This is a web app to allow users to perform bulk searching')

#Creating a File Uploader within Streamlit
upload_file = st.file_uploader('Upload a file containing checklist data in xlsx/csv format')

if upload_file is not None:
    #extension of file
    ext = os.path.splitext(upload_file.name)[1].lower()
    #Check the upload file extension and read the file to a dataframe using pandas
    if ext == '.xlsx':
        #xlsx
        df = pd.read_excel(upload_file)
    elif ext == '.csv':
        df = pd.read_csv(upload_file)
    else:
        err = "<font color='red'>error: the file not in xlsx/csv format</font>"
        st.markdown(f'<p style= "color:#ff0000;">error: the file not in xlsx/csv format</p>', unsafe_allow_html=True)
    #Create a section for the dataframe
    st.header('Import dataframe')
    
if st.button('Check Scameter'):
    st.write(scameterCheck(df))
    st.header('Return result')
    #Display and setup the return result dataframe
    st.dataframe(df)
    #Download button
    st.download_button("Download CSV",
                      df.to_csv(index=False),
                      mime='text/csv')
       
else:
    st.write('Yet run the searching script')        
