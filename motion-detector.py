import json
import logging
import os
import requests
import RPi.GPIO as GPIO
import sys
import time as tt
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

INPUT_PIN = int(os.environ.get("INPUT_PIN"))
BRIDGE_IP = os.environ.get("BRIDGE_IP")
USERNAME = os.environ.get("USERNAME")
LIGHT_ID = os.environ.get("LIGHT_ID")

logger = logging.getLogger('motion-detector')
hdlr = logging.FileHandler('motion-detector.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)

def turn_light_on():
    payload = json.dumps({"on": True})
    url = ("http://%s/api/%s/lights/%s/state" % (BRIDGE_IP,USERNAME,LIGHT_ID))
    response = requests.put(url, payload)
    if response.status_code != 200:
        logger.error(str(response.body))

def turn_light_off():
    payload = json.dumps({"on": False})
    url = ("http://%s/api/%s/lights/%s/state" % (BRIDGE_IP,USERNAME,LIGHT_ID))
    response = requests.put(url, payload)
    if response.status_code != 200:
        logger.error(str(response.body))

def wait(time=1):
    tt.sleep(time)

try:
    while True:
        if (GPIO.input(INPUT_PIN) == 0):
            # print "no intruders"
            # logger.info("no intruders")
            turn_light_off()
            wait(time=0.01)
        else:
            # print "intruders"
            # logger.warn("intruders")
            turn_light_on()
            wait(time=0.01)
except:
    e = sys.exc_info()[0]
    logger.error(e)
