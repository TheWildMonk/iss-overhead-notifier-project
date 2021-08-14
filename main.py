import requests
from smtplib import *
import time
from datetime import datetime

# Constants
MY_LAT = 123
MY_LONG = 123
EMAIL = "demo@email.com"
RECEIVER = "receiveremail@email.com"
password = "##########"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
iss_position = (iss_latitude, iss_longitude)


def iss_overhead(latitude, longitude):
    """Function to check whether the ISS position is in between
    +5 or -5 degrees of user's current position"""
    if (latitude-5, longitude-5) <= iss_position <= (latitude+5, longitude+5):
        if time_now.hour < sunset:
            with SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=password)
                connection.sendmail(from_addr=EMAIL, to_addrs=RECEIVER,
                                    msg="subject: ISS OVERHEAD\n\n"
                                        "Hey, look up, the ISS is over your head!")


# Parameters for Sunrise Sunset API
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

# Fetching Sunrise & Sunset data
response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

# Current time
time_now = datetime.now()

# While loop to run the program every 60s.
is_sunset = True
while is_sunset:
    if sunrise <= time_now.hour < sunset:
        is_sunset = False
    else:
        iss_overhead(MY_LAT, MY_LONG)
        time.sleep(60)
