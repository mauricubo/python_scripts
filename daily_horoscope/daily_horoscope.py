from bs4 import BeautifulSoup
import locale
from datetime import date
from unidecode import unidecode
import requests
from send_email import Email

# URL Example
# https://www.elpais.com.uy/eme/astros/horoscopo-del-miercoles-8-de-febrero-de-2023-por-susana-garbuyo

email = Email()

# Webpage info
locale.setlocale(locale.LC_TIME, 'es_UY.UTF-8')
today = date.today()

base = "https://www.elpais.com.uy"
path = f"/eme/astros/horoscopo-del-{today:%A}-{today.day}-de-{today:%B}" + \
            f"-de-{today:%Y}-por-susana-garbuyo"

# Crawling part
try:
    webpage = requests.get(unidecode(base+path))
    webpage.encoding = "utf-8"
    if(webpage.status_code != 200):
        raise Exception("Could not download the webpage due a connection error")
    soup = BeautifulSoup(webpage.text, 'html.parser')
    # The horoscopes are inside all that tags
    horoscopes = soup.select(selector="div.Page-content div.Page-twoColumn main.Page-main \
        div.Page-articleBody div.RichTextArticleBody p")

    # Find my horoscope
    for horoscope in horoscopes:
        tauro = horoscope.find("b")
        if tauro and tauro.string == "Tauro":
            # Build email message body
            message = f"""{tauro.string}
            {horoscope.find("br").next_sibling}"""
            subject = f"Horoscopo del {today:%A} {today.day} de {today:%B}"
            # Send the email
            sent = email.send_email(dest_to="mauricio.alpuin@gmail.com",
            subject=subject,
            message=message)
            if not sent:
                raise Exception("Couldn't send the email due a problem...")
except Exception as e:
    print("Failed to obtain the horoscope")
    print(e)