import urllib.request
import datetime
import time
import sys
import os
import tkinter
from datetime import datetime
from urllib.request import urlopen
from PIL import Image as Img
from wand.image import Image as Image1
from pynput.keyboard import Key, Controller

CURRENT_VERSION = "1.2"
LAST_UPDATE_TIME = "03.03.2020"

    # pharmacy on duty
url = 'https://www.istanbuleczaciodasi.org.tr/print/nobetciler_print.php?t=b&bid=28&d=0&z=17&map_show=1'

    # pharmacy on duty tomorrow
url2 = 'http://www.istanbuleczaciodasi.org.tr/print/nobetciler_print.php?t=b&bid=28&d=1&z=17&map_show=1'

application_path = os.path.join(os.environ["HOME"], "NöbetUygulaması")

keyboard = Controller()

AUTHOR_INFO = """
****NÖBETÇİ ECZANE UYGULAMASI****

    MUHAMMET EREN AYDIN
    Yazılım Tarihi: 30.9.2017
    Son Güncelleme Tarihi: {}
    Güncel Versiyon : {}""".format(LAST_UPDATE_TIME, CURRENT_VERSION)

    # Trying to enter google.com to check internet connection
	
def internet_accessible():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=5)
        return True
    except urllib.error.URLError:
        return False

	# Logging Errors

def log(string):

    dateTimeObj = datetime.now()
    print(string)
	# Add Timestamp
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
	# Append String to File
    with open(os.path.join(application_path, "logs.txt"), "a") as file:
        file.write(timestampStr + " -> \t" + string + "\n")

	# Taking PDF from Internet
		
def takepdf(url):

    file_name = os.path.join(application_path, "nobetciler_print.pdf")
    try:
        urllib.request.urlretrieve(url, file_name)
    except urllib.error.URLError:
        log("PDF alınamadı")
        time.sleep(10)
        return False

    # Converting PDF Pages to Pictures

    with Image1(filename=os.path.join(application_path, "nobetciler_print.pdf[0]")) as img:
        img.save(filename=os.path.join(
            application_path, "tempFiles", "temp.jpg"))
    with Image1(filename=os.path.join(application_path, "nobetciler_print.pdf[1]")) as img:
        img.save(filename=os.path.join(
            application_path, "tempFiles", "temp1.jpg"))

    file = open(os.path.join(application_path, "dayofmonth.txt"), "w")
    file.write(str(datetime.datetime.now().day))
    file.close()
    return True

def manipulate_jpg(x, y):
    # Opening Converted Images

    image1 = Img.open(os.path.join(application_path, "tempFiles", "temp.jpg"))
    image2 = Img.open(os.path.join(application_path, "tempFiles", "temp1.jpg"))

    # Concatenate images and change It's Position for Screen Sticking
    minNow = datetime.datetime.now().minute
    if minNow == 15 or minNow == 45:
        image = Img.new("RGB", (1490, 842))
        image.paste(image1, (200, 0))
        image.paste(image2, (795, 0))
        image = image.resize((x-4, y-34), 1)
        return image
    else:
        image = Img.new("RGB", (1490, 842))
        image.paste(image1, (150, 0))
        image.paste(image2, (745, 0))
        image = image.resize((x-4, y-34), 1)
        return image

	# Realise New Day Is Came
	
def timeComp():

    global url
    while True:
        file = open(os.path.join(application_path, "dayofmonth.txt"), 'r')
        dayofmonth = file.readline()
        file.close()
        if datetime.datetime.now().day != int(dayofmonth):
            if datetime.datetime.now().hour == 9 or datetime.datetime.now().hour == 18:
                if datetime.datetime.now().minute == 15:
                    time.sleep(70)
                    while not takepdf(url):
                        time.sleep(30)
                    display()

        minNow = datetime.datetime.now().minute
        if minNow == 0 or minNow == 15 or minNow == 30 or minNow == 45:
            display()
			
def display():

	# Remake the Picture and Display It Again
	global window_height, window_width
    image = manipulate_jpg(window_width,window_height)
    last_path = os.path.join(application_path, "last.jpg")
    image.save(last_path, "JPEG")
   
    os.system("sudo killall gpicview")
    os.popen("sudo gpicview " + last_path)
	
	# Full Screen
	keyboard.press(Key.f11)
	keyboard.release(Key.f11)

    # Test Internet Connection

