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

log_path = join(dirname(__file__), 'motion-detector.log')
logger = logging.getLogger('motion-detector')
hdlr = logging.FileHandler(log_path)
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
    logger.info(str(response.status_code))
    logger.info(str(response.json()))
    if response.status_code != 200:
        logger.error(str(response.json()))

def turn_light_off():
    payload = json.dumps({"on": False})
    url = ("http://%s/api/%s/lights/%s/state" % (BRIDGE_IP,USERNAME,LIGHT_ID))
    response = requests.put(url, payload)
    logger.info(str(response.status_code))
    logger.info(str(response.json()))
    if response.status_code != 200:
        logger.error(str(response.json()))

def wait(time=1):
    tt.sleep(time)

def init():
    turn_light_off()

    try:
        while True:
            if (GPIO.input(INPUT_PIN) == 0):
                logger.info("no motion detected")
                turn_light_off()
                wait(time=2)
            else:
                logger.warn("motion detected")
                turn_light_on()
                wait(time=2)
    except:
        e = sys.exc_info()[0]
        logger.error(e)

init()
