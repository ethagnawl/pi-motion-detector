import logging
import os
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

light_status = 0

logger = logging.getLogger('motion-detector')
hdlr = logging.FileHandler('motion-detector.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.ERROR)

GPIO.setmode(GPIO.BCM)
GPIO.setup(INPUT_PIN, GPIO.IN)

def turn_light_on():
    command = ("curl -X PUT -H \"Content-Type: application/json\" -d '{\"on\": true}' http://%s/api/%s/lights/%s/state" % (BRIDGE_IP, USERNAME, LIGHT_ID))
    os.system(command)

def turn_light_off():
    command = ("curl -X PUT -H \"Content-Type: application/json\" -d '{\"on\": false}' http://%s/api/%s/lights/%s/state" % (BRIDGE_IP, USERNAME, LIGHT_ID))
    os.system(command)

def wait(time=1):
    tt.sleep(time)

try:
    while True:
            i = GPIO.input(22)
            # print "i:", i
            if i == 0:
                    # print "no intruders"
                    # logger.info("no intruders")
                    if light_status == 1:
                        turn_light_off()
                        light_status = 0
                    wait(time=0.01)
            else:
                    # print "intruders"
                    # logger.warn("intruders")
                    if light_status == 0:
                        turn_light_on()
                        light_status = 1
                    wait(time=0.01)
except:
    e = sys.exc_info()[0]
    logger.error(e)
