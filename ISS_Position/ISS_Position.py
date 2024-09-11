import requests 
import json
import datetime
import time
import smtplib

username = "francesco.brunetti.k@gmail.com"
password = "nood glyd ejlp wbnn"
destination = "gestione.franci@gmail.com"

MY_LAT = 43.850960
MY_LONG = 10.981720

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
    }
# Function to get the current position of the ISS
def get_iss_position():
    # Make a request to the API
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    response.raise_for_status()
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Get the position of the ISS
        latitude = data['iss_position']['latitude']
        longitude = data['iss_position']['longitude']
        position = (latitude, longitude)
        print(f"The ISS current position at {datetime.datetime.now()} is {position[0]} latitude and {position[1]} longitude.")
        return position
    elif response.status_code == 429:
        print("Too many requests. Please wait a while before trying again.")
        return None
    elif response.status_code == 404:
        print("ISS position not found.")
        return None
    elif response.status_code == 503:
        print("ISS position service is unavailable.")
        return None
    else:
        # If the request was not successful, return None
        return None

def sunrise_sunset():
    # Make a request to the API
    url = "https://api.sunrise-sunset.org/json"
    response = requests.get(url, params=parameters)
    response.raise_for_status()
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        sunrise_h = int(data['results']['sunrise'].split("T")[1].split(":")[0])
        sunrise_m = int(data['results']['sunrise'].split("T")[1].split(":")[1])
        sunset_h = int(data['results']['sunset'].split("T")[1].split(":")[0])
        sunset_m = int(data['results']['sunset'].split("T")[1].split(":")[1])
        #print(f"The sunrise is at {sunrise_h}:{sunrise_m} and the sunset is at {sunset_h}:{sunset_m}.")
        return sunrise_h, sunset_h
    elif response.status_code == 429:
        print("Too many requests. Please wait a while before trying again.")
        return None
    elif response.status_code == 404:
        print("ISS position not found.")
        return None
    elif response.status_code == 503:
        print("ISS position service is unavailable.")
        return None
    else:
        # If the request was not successful, return None
        return None

def iss_overhead():
    if MY_LAT - 5 <= float(iss_pos[0]) <= MY_LAT + 5 and MY_LONG - 5 <= float(iss_pos[1]) <= MY_LONG + 5:
        print("The ISS is above you.")
        return True
    else:
        print("The ISS is not above you.")
        return False

def is_night():
    sun = sunrise_sunset()
    now = datetime.datetime.now().hour
    #print(f"The current time is {now}.")
    if (sun[1] < now) or (now < sun[0]):
        print("It's dark outside.")
        return True
    else:
        print("It's light outside.")
        return False

while True:
    while is_night():
        iss_pos = get_iss_position()
        if iss_overhead():
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=username, password=password)
                connection.sendmail(
                    from_addr=username,
                    to_addrs=destination,
                    msg=f"Subject:Look Up\n\nThe ISS is above you in the sky."
                    )
            break            
        else:
            time.sleep(5)



    
