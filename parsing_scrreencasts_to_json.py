import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import urllib
from time import sleep
import atexit

Username = ""
Password = ""
browser = webdriver.Firefox()
CurrentPage = 1
Links = []
MaxPage = 9

def saveToJSON():
    global browser
    prettyScreencast = json.dumps(Screencasts, sort_keys=True, indent=2, separators=(',', ': '))
    with open("screencasts.json", "w") as json_file:
        json_file.write(prettyScreencast)

atexit.register(saveToJSON)

def sign_in():
    global browser,Username,Password
    sign_in_url = "http://www.codeschool.com/users/sign_in"
    browser.get(sign_in_url)
    browser.find_element_by_id("user_login").clear()
    browser.find_element_by_id("user_login").send_keys(Username)
    browser.find_element_by_id("user_password").clear()
    browser.find_element_by_id("user_password").send_keys(Password)
    browser.find_element_by_xpath("//div[@id='sign-in-form']/form/div/div/button").click()

def goToScreenCastsPage():
    screencasts_url = "http://www.codeschool.com/screencasts"
    browser.get(screencasts_url)

def goToNextScreencastPage():
    global CurrentPage
    CurrentPage += 1
    browser.find_element_by_xpath("//a[@data-page='" + str(CurrentPage) + "']").click()

def readAScreenCast(link):
    global browser
    browser.get('https://codeschool.com' + link)
    html = browser.page_source
    soup = BeautifulSoup(html ,'lxml')
    return soup.find('a',{'class','tag'}).text, soup.find('span',{'class','has-tag--heading tci'}).text , soup.find('video')['src']

def getScreenCastLinksInCurrentPage():
    global Links,browser
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    for link in soup.find_all('a',{'class','twl'}):
        print "Added " + link['href'] + " to links"
        Links.append(link['href'])

sign_in()
goToScreenCastsPage()
sleep(1)
getScreenCastLinksInCurrentPage()
while (CurrentPage < MaxPage):
    goToNextScreencastPage()
    sleep(1)
    getScreenCastLinksInCurrentPage()

Screencasts = []
for index, link in enumerate(list(set(Links))):
    screencast = {
    "name":"",
    "url":"",
    "path":""
    }
    try:
        screencast['path'], screencast['name'], screencast['url'] = readAScreenCast(link)
    except (RuntimeError, TypeError, NameError):
        print "Error while trying to build link to " + link
        continue

    if screencast['path'] == "HTML/CSS":
        screencast['path'] = "HTML&CSS"
    elif screencast['path'] == ".NET":
        screencast['path'] = "dot NET"

    print screencast['name']
    Screencasts.append(screencast)
