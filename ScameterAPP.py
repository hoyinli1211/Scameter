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

#initialization of session state
if 'indEnd' not in st.session_state:
    st.session_state['ind0'] = False
    st.session_state['ind1'] = False
    st.session_state['ind2'] = False
    st.session_state['df']=[]

#st.write(st.session_state) 
    
#required function(s)
def scameterCheck(frame):
    if isinstance(frame, pd.DataFrame):
        #Input the weblink
        link = "https://cyberdefender.hk/en-us/"
               
        option = webdriver.ChromeOptions()
        option.add_argument('-headless')
        option.add_argument("--remote-debugging-port=2212")
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument("start-maximized")
        driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()), options=option)
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
            
            driver.set_window_size(1920, 1100)
            driver.get_screenshot_as_file(JobID + ".png")
            image = Image.open(JobID + ".png")
            image.save(JobID + ".png")
            vImage.append(JobID + ".png")
            st.image(image)
            
            #pdf
            pdf.add_page()
            pdf.set_margins(0,0,0)
            pdf.set_font("Arial", size=12)
            pdf.cell(20,10,JobID, 5,5,'C')
            width, height = Image.open(JobID + ".png").size
            width, height = float(width * 0.13), float(height * 0.13)
            pdf.image(JobID + ".png", 20 , 20, width, height)
            #pdf.line(x1=85, y1=27.5, x2=125, y2=27.5)
            
            #Result = driver.find_element_by_xpath('/html/body/form/section/div[2]/div[1]/div[2]/h1').text
            #risk = driver.find_element_by_xpath('/html/body/form/section/div[2]/div[1]/div[1]/img').get_attribute("src").rsplit('/', 1)[-1]
            Result = driver.find_element(By.XPATH, '/html/body/form/section/div[2]/div[1]/div[2]/h1').text
            risk = driver.find_element(By.XPATH, '/html/body/form/section/div[2]/div[1]/div[1]/img').get_attribute("src").rsplit('/', 1)[-1]
            RiskRating = re.sub("_en.webp", "", risk)
            
            frame['Result'].iloc[i] = Result
            frame['RiskRating'].iloc[i] = RiskRating
            frame['JobID'].iloc[i] = JobID
        
        pdf.output('output1.pdf','F')
        
    else: print("input not dataframe")

# Add a title and intro text
st.title('Bulk checking on Scameter')
st.text('This script is for educational purpose.')
st.text('This Web app allow users to perform bulk searching of ADCC tool Scameter.')
st.text('For details of the tool, please visit https://cyberdefender.hk/en-us/')

#Creating a File Uploader within Streamlit
st.header('STEP 1. Import the data with Column Value')
upload_file = st.file_uploader('Upload a file containing checklist data in xlsx/csv format. Template file available below.')

if upload_file is not None:
    st.session_state['ind0'] = True
else:
    pass

temp_file = 'template.xlsx'
df_temp = pd.read_excel(temp_file)
st.download_button("Download template file",
                      df_temp.to_csv(index=False),
                      mime='text/csv')

if st.session_state['ind0']==False:
    st.header('STEP 2. Review the imported dataframe')
    st.header('STEP 3. Check the Scameter')  
    #st.write(st.session_state) 
elif st.session_state['ind0']==True:
    if st.session_state['ind1']==False:
        #extension of file
        ext = os.path.splitext(upload_file.name)[1].lower()
        #Check the upload file extension and read the file to a dataframe using pandas
        if ext == '.xlsx':
            #xlsx
            df = pd.read_excel(upload_file, dtype=str)
        elif ext == '.csv':
            df = pd.read_csv(upload_file, dtype=str)
        else:
            err = "<font color='red'>error: the file not in xlsx/csv format</font>"
            st.markdown(f'<p style= "color:#ff0000;">error: the file not in xlsx/csv format</p>', unsafe_allow_html=True)
        #Create a section for the dataframe
        st.header('STEP 2. Review the imported dataframe')
        st.write(df)
        df=df
        st.header('STEP 3. Check the Scameter')
        st.session_state['ind1'] = True
        #st.write(st.session_state) 
    else:
        df=st.session_state['df']

#if st.session_state['ind0']==True and st.session_state['ind1']==True and st.session_state['ind2']==False and st.session_state['end']!=True:
if True==True:
    if st.button('Check Scameter'):
        pdf = FPDF('L', 'mm', 'A4') #create an A-4 size pdf document
        vImage = []
        st.write(scameterCheck(df))
        st.header('Return result')
        #Display and setup the return result dataframe
        st.dataframe(df)
        df=df
        st.session_state['df']=df
        vImage = vImage
        ind2=True
        st.session_state['ind2'] = True
        st.session_state['indEnd'] = True
        #st.write(st.session_state)
    else:
        pass
elif st.session_state['ind2']==True:
    st.write("Result already executed. Please refresh the page for checking next batch")
    #st.write(st.session_state) 

st.header('STEP 4. Export return result and audit log on screenshot after review')
if (st.session_state['ind1']==True and st.session_state['ind2']==True and st.session_state['indEnd'] == True):
    #st.write(st.session_state['df'])
    df = st.session_state['df']
    df['Value'] = df['Value'].astype("string")
    st.write(df)
    df_xlsx = df.to_excel("output.xlsx")
    st.download_button("Download Output",
                       #data=df.to_csv(index=False, header=True),
                       data=df_xlsx,
                       mime='text/csv') 
    with open("output1.pdf", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    st.download_button("Download Image screenshot PDF",
                       data=PDFbyte,
                       file_name="audittrail.pdf",
                       mime='application/octet-stream') 
    #st.write(st.session_state) 
else:
    pass
    #st.write(st.session_state) 

clearAll = st.button("Clear All")    
if clearAll:
    if 'indEnd' in st.session_state:
        del st.session_state['indEnd']
    else:
        pass

#End of Script
