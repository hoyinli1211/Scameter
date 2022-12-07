#20221204 - First attempt using streamlit
#Ref: https://towardsdatascience.com/getting-started-with-streamlit-web-based-applications-626095135cb8

#import required library
import streamlit as st
import os, sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime, timedelta, date
import math
import requests
import numpy as np
import re
from PIL import Image
import glob
import cv2
import zipfile
from fpdf import FPDF

#required function
def scameterCheck(frame):
    if isinstance(frame, pd.DataFrame):
        #Input the weblink
        link = "https://cyberdefender.hk/en-us/"
        
        #Create instance of chrome
        #firefoxOptions = Options()
        #firefoxOptions.add_argument("--headless")
        #driver = webdriver.Firefox(
        #    options=firefoxOptions,
        #    executable_path="/home/appuser/.conda/bin/geckodriver",
        #)
        
        option = webdriver.ChromeOptions()
        #options.add_argument("--window-size=1920,1080")
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        option.add_argument('-headless')
        option.add_argument("--remote-debugging-port=2212")
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument("start-maximized")
        driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=option)
        #driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(0.5)
        
        frame['JobID'] = ""
        
        for i in range(frame.count()[0]):
            JobID = date.today().strftime("%Y%m%d") + str(i+1).zfill(3)
            st.write(JobID)
            value = frame['Value'].iloc[i]
            #Open the link
            driver.get(link)
            time.sleep(3)
            
            #Clear the value of search bar and input new value
            driver.find_element_by_id('search').clear()
            driver.find_element_by_id('search').send_keys(value)

            #Click the submit button
            #driver.find_element_by_xpath('//*[@id="post-3646"]/div/div/section[2]/div/div/div/div/div/form/div/div/div[1]/div[2]/div[2]').click()
            driver.find_element(By.XPATH, '//*[@id="post-3646"]/div/div/section[2]/div/div/div/div/div/form/div/div/div[1]/div[2]/div[2]').click()
            time.sleep(5)
            
            driver.set_window_size(1920, 1200)
            driver.get_screenshot_as_file(JobID + ".png")
            image = Image.open(JobID + ".png")
            image.save(JobID + ".png")
            vImage.append(JobID + ".png")
            lImage.append(image)
            st.image(image)
            pdf.add_page()
            pdf.image(JobID + ".png", 60,120,w=120) 
            
            #Result = driver.find_element_by_xpath('/html/body/form/section/div[2]/div[1]/div[2]/h1').text
            #risk = driver.find_element_by_xpath('/html/body/form/section/div[2]/div[1]/div[1]/img').get_attribute("src").rsplit('/', 1)[-1]
            Result = driver.find_element(By.XPATH, '/html/body/form/section/div[2]/div[1]/div[2]/h1').text
            risk = driver.find_element(By.XPATH, '/html/body/form/section/div[2]/div[1]/div[1]/img').get_attribute("src").rsplit('/', 1)[-1]
            RiskRating = re.sub("_en.webp", "", risk)
            
            frame['Result'].iloc[i] = Result
            frame['RiskRating'].iloc[i] = RiskRating
            frame['JobID'].iloc[i] = JobID
        
        #Save all images to a pdf file
        
        #for image_url in vImage:
        #    pdf.add_page()
        #    pdf.image(image_url, 0,0,200,250) 
                   
    else: print("input not dataframe")

# Add a title and intro text
st.title('Bulk checking on Scameter')
st.text('This script is for educational purpose.')
st.text('This Web app allow users to perform bulk searching of ADCC tool Scameter.')
st.text('For details of the tool, please visit https://cyberdefender.hk/en-us/')

#Creating a File Uploader within Streamlit
st.header('STEP 1. Import the data with Column Value')
upload_file = st.file_uploader('Upload a file containing checklist data in xlsx/csv format. Template file available below.')

temp_file = 'template.xlsx'
df_temp = pd.read_excel(temp_file)
st.download_button("Download template file",
                      df_temp.to_csv(index=False),
                      mime='text/csv')

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
    st.header('STEP 2. Review the imported dataframe')
    st.write(df)
    st.header('STEP 3. Check the Scameter')
    
if st.button('Check Scameter'):
    pdf = FPDF() #create an A-4 size pdf document
    vImage = []
    lImage = []
    st.write(scameterCheck(df))
    st.header('Return result')
    #Display and setup the return result dataframe
    st.dataframe(df)
    #Download button for the output csv
    st.download_button("Download CSV",
                        df.to_csv(index=False),
                        mime='text/csv')
    #Download button for the screenshot for audit purpose
    pdf2 = FPDF('P', 'mm', 'A4')
    pdf3 = FPDF()
    for i in vImage:
        pdf2.add_page()
        pdf2.set_margins(0,0,0)
        pdf2.output('output.pdf','F')
        pdf2.set_font("Arial", size=12)
        pdf2.cell(50,50,i, 0,0,'C')
        pdf2.image(i)
        pdf2.line(x1=85, y1=27.5, x2=125, y2=27.5)
        pdf2.output('output.pdf','F')
    
    st.download_button("Download Image screenshot PDF",
                       data=pdf2.output(dest='S'),
                       file_name="audittrail.pdf",
                       mime='application/octet-stream')       
else:
    st.write('Yet run the searching script')        
