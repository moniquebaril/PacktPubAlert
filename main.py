import urllib.request
from bs4 import BeautifulSoup
from slacker import Slacker
from local_settings import *
import os.path
import json

url = "https://www.packtpub.com/packt/offers/free-learning"
packt_logo = "https://lh3.googleusercontent.com/uKQyBaMg2GjonsxqYsp8CitgG8usmFpBUsbg1BuppjGsrOyV02gD4fVxxCOh29QAW3NZ7rE=s85"
channel = "#packtalert"


def get_url_contents():
    try:
        opener = urllib.request.FancyURLopener({})
        f = opener.open(url)
        content = f.read()
        return content
    except BaseException as e:
        print(str(e))
        return ""


def find_description():
    section = soup.find("div", class_="dotd-main-book-summary float-left")
    section_soup = BeautifulSoup(str(section), 'html.parser')
    desc = section_soup.get_text().strip()
    countdown_message = "Time is running out to claim this free ebook"
    if str(desc).startswith(countdown_message):
        desc = desc.replace(countdown_message, "").strip()
    if str(desc).startswith(title):
        desc = desc[len(title):].strip()
    while "\n\n" in desc:
        desc = desc.replace("\n\n", "\n")
    desc = desc.replace("\n", "\n>")
    desc = ">" + desc
    if desc == ">":
        return ""
    return desc + "\n"


def send_slack_alert(slack_message):
    slack_client = Slacker(SLACK_API_TOKEN)
    try:
        return slack_client.chat.post_message(channel, slack_message, "packtBot",
                                              None, None, None, None, None, None, packt_logo)
    except BaseException as e:
        print(str(e))
        return ""


def get_last_book_seen():
    try:
        if os.path.isfile(FILE_HISTORY):
            with open(FILE_HISTORY, "r") as file:
                return file.read().replace("title=", "")
    except BaseException as e:
        print(str(e))
        return ""


def update_last_book_seen(current_title):
    try:
        with open(FILE_HISTORY, "w") as file:
            file.write("title=" + current_title)
    except BaseException as e:
        print(str(e))


html = get_url_contents()
if html == "":
    print("Could not download html for the given url")
    exit()
title = ""
try:
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find("h2").string.strip()
except BaseException as e:
    print(str(e))
    exit()
description = find_description()
last_book_seen = get_last_book_seen()
message = "Today's title is *" + title + "*\n" + description + url
if last_book_seen == title:
    print("This message has already been sent to Slack, message will not be sent")
    print(message)
else:
    print("This is a new book - alert has not yet been sent, sending alert")
    response = str(send_slack_alert(message))
    if response != "":
        response = json.loads(response)
        if response["ok"]:
            update_last_book_seen(title)
    else:
        print("Error sending slack message")
