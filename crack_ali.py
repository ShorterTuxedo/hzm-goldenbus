import requests
import json
import time
import random
from urllib import parse
import requests
# TRACK = ""

def slide(session, headers, referrerURL, APPID, scene, ncSessionID, TRACK):
    try:
        mySlider = requests.post("http://localhost:8001/captcha", json={
            "appId": APPID,
            "scene": scene
        }).json()
        print("验证码破解成功")
        return mySlider
    except Exception:
        print("验证码破解失败")
        return None