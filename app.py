#!/usr/bin/env python

from flask import Flask, request, jsonify,render_template
import requests
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import urllib
import csv
import time
import shutil
import os
import json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import fromstring
from xmljson import badgerfish as bf
from random import sample

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/scrape', methods=['POST'])
def post():
    postcast_url = {
        "postcast_url1" : request.form['postcast_url1'],
        "postcast_url2" : request.form['postcast_url2'],
        "postcast_url3" : request.form['postcast_url3'],
        "postcast_url4" : request.form['postcast_url4'],
        "postcast_url5" : request.form['postcast_url5'],
        "postcast_url6" : request.form['postcast_url6'],
        "postcast_url7" : request.form['postcast_url7'],
        "postcast_url8" : request.form['postcast_url8'],
        "postcast_url9" : request.form['postcast_url9'],
        "postcast_url10" : request.form['postcast_url10']
    }

    postcast_result = {
        "postcast_url1" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url2" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url3" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url4" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url5" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url6" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url7" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url8" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url9" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
        "postcast_url10" : {"title" : "", "author" : "", "email" : "", "feed_url" : ""},
    }
    #Loop for URLs
    for x in range(10):
        if postcast_url["postcast_url"+str(x+1)] != "":
            #Get the path of download directory
            print (x)
            if os.name == 'nt':
                import ctypes
                from ctypes import windll, wintypes
                from uuid import UUID

                # ctypes GUID copied from MSDN sample code
                class GUID(ctypes.Structure):
                    _fields_ = [
                        ("Data1", wintypes.DWORD),
                        ("Data2", wintypes.WORD),
                        ("Data3", wintypes.WORD),
                        ("Data4", wintypes.BYTE * 8)
                    ] 

                    def __init__(self, uuidstr):
                        uuid = UUID(uuidstr)
                        ctypes.Structure.__init__(self)
                        self.Data1, self.Data2, self.Data3, \
                            self.Data4[0], self.Data4[1], rest = uuid.fields
                        for i in range(2, 8):
                            self.Data4[i] = rest>>(8-i-1)*8 & 0xff

                SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
                SHGetKnownFolderPath.argtypes = [
                    ctypes.POINTER(GUID), wintypes.DWORD,
                    wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
                ]

                def _get_known_folder_path(uuidstr):
                    pathptr = ctypes.c_wchar_p()
                    guid = GUID(uuidstr)
                    if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
                        raise ctypes.WinError()
                    return pathptr.value

                FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

                def get_download_folder():
                    return _get_known_folder_path(FOLDERID_Download)
            else:
                def get_download_folder():
                    home = os.path.expanduser("~")
                    return os.path.join(home, "Downloads")

            down_folder_path = get_download_folder()
            # Remove a old file
            if os.path.isfile(down_folder_path + "/" + "1.txt"):
                os.remove(down_folder_path + "/" + "1.txt")
                print("[" + str(datetime.now()) + "]" + "-INFO" + ": Old text file is removed !")

            print("[" + str(datetime.now()) + "]" + "-INFO" + ": -----URL: " + postcast_url["postcast_url"+str(x+1)] + "------")
            url = postcast_url["postcast_url"+str(x+1)]

            # Configure Chrome Web Driver
            chrome_options = webdriver.ChromeOptions()
            prefs = {"profile.default_content_setting_values.notifications" : 2}
            chrome_options.add_experimental_option("prefs",prefs)
            driver = webdriver.Chrome("/Users/khristianmarcial/FTF/scraper/PythonScraper/chromedriver")
            driver.set_page_load_timeout("10")
            driver.set_window_size(1341,810)
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": Chrome Web Driver is ready.")

            # Extract id
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": Extracting ID ...")
            try:
                driver.get(url)
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'apple:content_id')))
                print ("[" + str(datetime.now()) + "]" + "-INFO" + ": Page is ready!")
            except TimeoutException:
                try:
                    driver.refresh()
                    print ("[" + str(datetime.now()) + "]" + "-INFO" + ": Loading took too much time! Retrying...")
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'apple:content_id')))
                    print ("[" + str(datetime.now()) + "]" + "-INFO" + ": Page is ready!")
                except TimeoutException:
                    print ("[" + str(datetime.now()) + "]" + "-INFO" + ": Loading took too much time!")

            id = driver.find_element_by_name("apple:content_id").get_attribute("content")
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": ID is " + id)
            time.sleep(2)



            # Download txt
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": Downloading a text file...")
            download_url = "https://itunes.apple.com/lookup?id=" + id + "&entity=podcast"
            driver.get(download_url)
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": Downloaded successfully !")
            time.sleep(5)
            driver.close()

            # Read txt
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": Reading a text file...")
            f=open(down_folder_path + "/" + "1.txt", "r")
            if f.mode == 'r':
                txt =f.read()

            txt_json = json.loads(txt)

            feed_url = txt_json['results'][0]['feedUrl']
            
            print("[" + str(datetime.now()) + "]" + "-INFO" + ": FeedURL : " + feed_url)

            # Parse XML
            xml_reponse = requests.get(feed_url)

            json_response = bf.data(fromstring(xml_reponse.content))

            postcast_result["postcast_url"+str(x+1)]["feed_url"] = feed_url

            print(json_response["rss"]["channel"]["title"]["$"])
            postcast_result["postcast_url"+str(x+1)]["title"] = json_response["rss"]["channel"]["title"]["$"]

            print(json_response["rss"]["channel"]["{http://www.itunes.com/dtds/podcast-1.0.dtd}author"]["$"])
            postcast_result["postcast_url"+str(x+1)]["author"] = json_response["rss"]["channel"]["{http://www.itunes.com/dtds/podcast-1.0.dtd}author"]["$"]

            print(json_response["rss"]["channel"]["{http://www.itunes.com/dtds/podcast-1.0.dtd}owner"]["{http://www.itunes.com/dtds/podcast-1.0.dtd}email"]["$"])
            postcast_result["postcast_url"+str(x+1)]["email"] = json_response["rss"]["channel"]["{http://www.itunes.com/dtds/podcast-1.0.dtd}owner"]["{http://www.itunes.com/dtds/podcast-1.0.dtd}email"]["$"]

            f.close()
            time.sleep(5)

    table = pd.DataFrame.from_dict(postcast_result, orient="index")
    table.to_csv("postcast_scrape.csv")
    return render_template("success.html", alert_text = "Scraped Successfully !", postcast_result = postcast_result)

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=3030)