import urllib.request
from bs4 import BeautifulSoup
from slacker import Slacker
from local_settings import *

url = "https://www.packtpub.com/packt/offers/free-learning"
packt_logo = "https://lh3.googleusercontent.com/uKQyBaMg2GjonsxqYsp8CitgG8usmFpBUsbg1BuppjGsrOyV02gD4fVxxCOh29QAW3NZ7rE=s85"


def get_url_contents():
    opener = urllib.request.FancyURLopener({})
    f = opener.open(url)
    content = f.read()
    return content


def find_description():
    section = soup.find("div", class_="dotd-main-book-summary float-left")
    for tag in section:
        if str(tag).startswith("<div>"):
            return str(tag).replace("<div>", "").replace("</div>", "").strip()


def send_slack_alert(message):
    slack_client = Slacker(SLACK_API_TOKEN)
    slack_client.chat.post_message("packtalert", message, "packtBot", None, None, None, None, None, None, packt_logo)


html = get_url_contents()
soup = BeautifulSoup(html, 'html.parser')
title = soup.find("h2").string.strip()
description = find_description()
send_slack_alert("Today's title: *" + title + "*\n>" + description + "\n" + url)

