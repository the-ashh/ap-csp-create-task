import smtplib
import time
import pyowm
import time
import datetime

owm = pyowm.OWM('owm api jey') 

def sendMail(to, message):
    password = "password"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("email@example com", password)
    server.sendmail("email@example.com", to, message)
    server.quit()
    print("sent \"" + message + "\"")
    
def kelvinToFarenheit(temp):
    return (temp - 273.15) * (9 / 5) + 32
    
def epochToDate(epoch):
    return time.strftime('%H:%M', time.localtime(epoch))

def formatWeatherMessage(weatherArray, currentStatus):
    message = "hey aus! here's the daily weather report~ "
    i = 0
    if "rain" in currentStatus: recommendation = "i would recommend a jacket today."
    elif "snow" in currentStatus: recommendation = "i would recommend a coat today."
    else: recommendation = ""
    while i < len(weatherArray):
        message = message + "\nat {}, there will be {}.".format(weatherArray[i], weatherArray[i + 1])
        i += 2
    message = message + """\ncurrent weather: {}. {}
have a good day~""".format(currentStatus, recommendation)
    return message

def getWeatherAndFormat(cityName):
    forecast = owm.three_hours_forecast(cityName).get_forecast()
    observation = owm.weather_at_place(cityName).get_weather()
    currentStatus = observation.get_detailed_status()
    i = 0
    weather = []
    for status in forecast:
        time = epochToDate(status.get_reference_time())
        weather.append(time)
        weather.append(status.get_detailed_status())
        i += 2
        if i > 14: break
    return formatWeatherMessage(weather, currentStatus)
    
def sendWeather(to, place):
    message = getWeatherAndFormat(place)
    sendMail(to, message)


sendMail("email@example.com", "weather notifier has started up~")

while True:
    currentTime = datetime.datetime.now()
    if currentTime.hour == 7 or currentTime.hour == 7:
        message = getWeatherAndFormat("New York, us")
        sendMail("email@example.com", message)
        time.sleep(86400)
        continue
    time.sleep(3600)
