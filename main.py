import requests
from smtplib import *
import time
from datetime import datetime

# Constants
MY_LAT = 23.761686
MY_LONG = 90.434939
MY_POSITION = (MY_LAT, MY_LONG)
EMAIL = "thewildmonk.python@gmail.com"
TEST_EMAIL = "thewildmonk@yahoo.com"
password = "Abcd1234()"

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
                connection.sendmail(from_addr=EMAIL, to_addrs=TEST_EMAIL,
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

time_now = datetime.now()
# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
is_sunset = True
while is_sunset:
    if sunrise <= time_now.hour < sunset:
        is_sunset = False
    else:
        iss_overhead(MY_LAT, MY_LONG)
        time.sleep(60)
