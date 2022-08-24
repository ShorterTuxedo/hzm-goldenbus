import requests
import json
import time
import random
from urllib import parse

# TRACK = ""

def slide(session, headers, referrerURL, APPID, scene, ncSessionID, TRACK):
    # global TRACK
    headers2 = headers
    headers2["Referer"] = referrerURL
    headers2["accept"] = "*/*"
    headers2.pop("content-type", None)
    captcha = session.get("https://ynuf.aliapp.org/w/wu.json", headers=headers2)
    UMIDTOKEN = captcha.text
    # print(UMIDTOKEN)
    UMIDTOKEN = captcha.text.split("umx.wu('")[1].split("');}catch")[0]
    # print("UMID TOKEN 是",UMIDTOKEN)
    # print(len(UMIDTOKEN))
    C_TOKEN = APPID + ":" + scene + ":" + str(int(time.time())) + ":" + str(random.random())
    init_payload = {
        "a": APPID,
        "t": C_TOKEN,
        "scene": scene,
        "lang": "cn",
        "v": "v1.2.20",
        "href": referrerURL,
        "comm": "{}",
        "callback": "initializeJsonp_" + "".join(str(random.random()).split("."))
    }
    INIT_URL = "https://cf.aliyun.com/nocaptcha/initialize.jsonp?" + parse.urlencode(init_payload)
    captcha = session.get(INIT_URL, headers=headers2)
    # print(captcha.text)
    analyze_payload = {
        "a": APPID,
        "t": C_TOKEN,
        "n": TRACK,
        "p": {
            "umidToken": UMIDTOKEN,
            "ncSessionID": ncSessionID
        },
        "scene": scene,
        "asyn": 0,
        "lang": "cn",
        "v": 1,
        "callback": "jsonp_" + "".join(str(random.random()).split("."))
    }
    ANALYZE_URL = "https://cf.aliyun.com/nocaptcha/analyze.jsonp?" + parse.urlencode(analyze_payload)
    captcha = session.get(ANALYZE_URL, headers=headers2)
    # print(captcha.text)
    myResult = json.loads(captcha.text.split("(")[1].split(")")[0])
    if myResult["result"]["code"] == 300:
        print("验证码破解失败")
        return None
    else:
        print("验证码破解成功")
    # if myResult[]
    captcha_params = {
        "sessionId": myResult["result"]["csessionid"],
        "sig": myResult["result"]["value"],
        "token": C_TOKEN
    }
    print(captcha_params)
    return captcha_params