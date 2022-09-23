import requests
import threading
import time
import sys
import datetime
import ddddocr
import json
import smtplib
import crack_ali
import acw_sc_v2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from urllib import parse
import os 
nowtime = datetime.datetime.now().strftime("%Y_%m_%d_%H:%M:%S")
logfile = f"log{nowtime}.txt"

TIMESHUA = False

CWRONG = False

# 00 = 成人 , 01 = 儿童
# 请使用港币支付
# 需要于 8：00 前几分钟运行。

CAPTCHA = 2 # 2 = 阿里云， 1 = 文字

info = json.loads(open("info.json", "r").read())

DATE = "1970-01-01" # 替代日期

def ticket_success(hzmbus, oheaders, orderNo, oReqNo):
    global DATE
    global info
    myLBox = ""
    if info.get("autopay", False):
        AUTH = oheaders["Authorization"]
        headers = oheaders
        """while True:
            try:
                homepage = hzmbus.post("https://i.hzmbus.com/webh5api/manage/get.payment.type.info", headers=headers, json={
                    "appId": "HZMBWEB_HK",
                    "currency": "2",
                    "joinType": "WEB",
                    "version": "2.7.202207.1213",
                    "equipment": "PC"
                });print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                time.sleep(time_wait)
                if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                    print("arg1="+arg1)
                    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                    print("acw_sc__v2="+ACWSCV2)
                    acw = requests.cookies.RequestsCookieJar()
                    acw.set("acw_sc__v2", ACWSCV2)
                    hzmbus.cookies.update(acw)
                    continue
                if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                    pass
                elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                    if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                        time.sleep(60)
                if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                    writeLog("[被限速] 要等一会儿。")
                    # time.sleep(30*60) # 等 30 分
                    continue
                homepage.json()
                break
            except Exception:
                continue"""
        MASTERCARD = "MasterCard" # homepage.json()["responseData"][0]["payCode"] # 我们用万事达信用卡支付
        while True:
            try:
                homepage = hzmbus.post("https://i.hzmbus.com/webh5api/wx/query.wx.order.payreq", headers=headers, json={
                    "orderNo": orderNo,
                    "payType": MASTERCARD,
                    "language":"lang-zh",
                    "feeType":9,
                    "currency":"2",
                    "appId":"HZMBWEB_HK",
                    "joinType":"WEB",
                    "version":"2.7.202207.1213",
                    "equipment":"PC"
                    });print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                # time.sleep(time_wait)
                if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                    print("arg1="+arg1)
                    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                    print("acw_sc__v2="+ACWSCV2)
                    acw = requests.cookies.RequestsCookieJar()
                    acw.set("acw_sc__v2", ACWSCV2)
                    hzmbus.cookies.update(acw)
                    continue
                if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                    pass
                elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                    if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                        time.sleep(60)
                if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                    writeLog("[被限速] 要等一会儿。")
                    # time.sleep(30*60) # 等 30 分
                    continue
                homepage.json()
                break
            except Exception:
                continue
        paymentData = {
            "merchant": json.loads(homepage.json()["json"])["merchant"],
            "interaction": json.loads(homepage.json()["json"])["interaction"],
            "sessionId": homepage.json()["responseData"]["sessionId"],
            "successId": homepage.json()["responseData"]["successId"],
            "orderNo": orderNo,
            "orderReqNo": oReqNo,
            "payType": MASTERCARD
        }  
        beitsin = requests.Session() # 卑钱
        """headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?1", # "?0",
            "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        while True:
            try:
                homepage = beitsin.get("https://mpgsproxy.hzmbus.com/checkout/hostedCheckout", headers=headers);print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                # time.sleep(time_wait)
                if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                    print("arg1="+arg1)
                    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                    print("acw_sc__v2="+ACWSCV2)
                    acw = requests.cookies.RequestsCookieJar()
                    acw.set("acw_sc__v2", ACWSCV2)
                    hzmbus.cookies.update(acw)
                    continue
                if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                    pass
                elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                    if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                        time.sleep(60)
                # if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                #    writeLog("[被限速] 要等一会儿。")
                #    # time.sleep(30*60) # 等 30 分
                #    continue
                # homepage.json()
                if not "Hosted Checkout" in str(homepage.content, encoding="UTF-8"):
                    continue
                break
            except Exception:
                continue"""
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "authorization": "",
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
            "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?1", # "?0",
            "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "Referer": "https://i.hzmbus.com/webhtml/login",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        while True:
            try:
                homepage = beitsin.post("https://mpgsproxy.hzmbus.com/api/page/version/56/pay", headers=headers, data={
                    'merchant': paymentData["merchant"],
                    'interaction.operation': 'PURCHASE',
                    'interaction.merchant.name': 'HZMB',
                    'interaction.locale': 'zh',
                    'interaction.cancelUrl': 'urn:hostedCheckout:defaultCancelUrl',
                    'interaction.timeoutUrl': 'urn:hostedCheckout:defaultTimeoutUrl',
                    'session.id': paymentData["sessionId"],
                });print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                # time.sleep(time_wait)
                if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                    print("arg1="+arg1)
                    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                    print("acw_sc__v2="+ACWSCV2)
                    acw = requests.cookies.RequestsCookieJar()
                    acw.set("acw_sc__v2", ACWSCV2)
                    hzmbus.cookies.update(acw)
                    continue
                if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                    pass
                elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                    if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                        time.sleep(60)
                if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                    writeLog("[被限速] 要等一会儿。")
                    # time.sleep(30*60) # 等 30 分
                    continue
                homepage.json()
                break
            except Exception:
                continue
        myRetURL = "https://mpgsproxy.hzmbus.com/checkout/api/returnUrl/" + paymentData["sessionId"]
        while True:
            try:
                writeLog("[RetURL] Getting RetURL.")
                homepage = beitsin.post(myRetURL, headers=headers, data={
                    "merchantId": paymentData["merchant"],
                    "returnUrl": "https://i.hzmbus.com/webhtml/order_details?orderNo="+paymentData["orderNo"]+"&tab1=1"
                });print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                # time.sleep(time_wait)
                if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                    print("arg1="+arg1)
                    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                    print("acw_sc__v2="+ACWSCV2)
                    acw = requests.cookies.RequestsCookieJar()
                    acw.set("acw_sc__v2", ACWSCV2)
                    hzmbus.cookies.update(acw)
                    continue
                if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                    pass
                elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                    if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                        time.sleep(60)
                # if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                #    writeLog("[被限速] 要等一会儿。")
                #    # time.sleep(30*60) # 等 30 分
                #    continue
                # homepage.json()
                if str(homepage.content, encoding="UTF-8") == "true":
                    break
                break
            except Exception:
                continue
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9",
            "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
            "sec-ch-ua-mobile": "?1", # "?0",
            "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        myLBox = "https://mpgsproxy.hzmbus.com/checkout/lightboxEntry/" + paymentData["sessionId"]
        writeLog(f"[支付链接] 如果您未检查电邮，支付链接在此：[{myLBox}]")
    print("Bought ticket")
    myDates = DATE
    myEmailContent = open("HZMB_Success_Email.html", "r", encoding="UTF-8").read()
    myEmailContent = myEmailContent.replace("[INSERT DATES HERE]", myDates)
    if info.get("autopay", False):
        myEmailContent = myEmailContent.replace("交付车费。", f"交付车费。<a href=\"{myLBox}\">点我支付</a>")
    myEmailTContent = open("HZMB_Success_Email.txt", "r", encoding="UTF-8").read()
    myEmailTContent = myEmailTContent.replace("[INSERT DATES HERE]", myDates)
    if info.get("autopay", False):
        myEmailContent = myEmailContent.replace("交付车费。", f"交付车费。[{myLBox}]")
    # 在这里输入 STMP 密码
    sender = info["mysendemail"] # 您的电邮
    receivers = info["emailreceivers"]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEMultipart('alternative')
    subject = '您抽到了健康驿站！'
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ";".join(receivers)

    part1 = MIMEText(myEmailTContent, 'plain', 'utf-8')
    part2 = MIMEText(myEmailContent, 'html', 'utf-8')
    
    message.attach(part1)
    message.attach(part2)
    
    try:
        smtpObj = smtplib.SMTP_SSL(info["smtphost"], info["smtpport"])
        smtpObj.ehlo()
        # stmpObj.starttls()
        smtpObj.login(info["mysendemail"], info["smtppwd"])
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")
    
def ticket_failure():
    print("Couldn't buy ticket")

def appendToDict(_dict, k, v):
    _dict[k] = v

def writeLog(text):
  _text="["+time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(time.time()))+"] "+text
  print(_text)
  log = open(logfile, "a", encoding="UTF-8")
  myLog = (_text+"\n")
  log.write(myLog)
  log.close()

myHeaders = [[None, {}] for i in range(len(info["monitors"]))] # 多账号查询余票
rateLimited = [None for i in range(len(info["monitors"]))] # 多账号查询余票
allRate = [True for i in range(len(info["monitors"]))]

def checkAll():
    global rateLimited
    for rateLimit in rateLimited:
        if rateLimit == None:
            return False
        if time.time() - rateLimit > 60:
            return False
    return True

mainAccHeaders = {}
"""
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?1", # "?0",
    "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
  }

hzmbus = requests.Session()

writeLog("="*20+"开始运行 (自动选日期)"+"="*20)

homepage = hzmbus.get("https://i.hzmbus.com/webhtml/login", headers=headers)

if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
    print("arg1="+arg1)
    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
    print("acw_sc__v2="+ACWSCV2)
    acw = requests.cookies.RequestsCookieJar()
    acw.set("acw_sc__v2", ACWSCV2)
    hzmbus.cookies.update(acw)

hzmbus.get("https://i.hzmbus.com/", headers=headers)
    
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "authorization": "",
    "content-type": "application/json;charset=UTF-8",
    "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?1", # "?0",
    "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Referer": "https://i.hzmbus.com/webhtml/login",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

while True:
    try:
        homepage = hzmbus.post("https://i.hzmbus.com/webh5api/login", headers=headers, json={
            "webUserid": info["uname"],
            "passWord": info["pwd"],
            "code":"",
            "appId":"HZMBWEB_HK",
            "joinType":"WEB",
            "version":"2.7.202207.1213",
            "equipment":"PC"
            }, timeout=1);print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))#;time.sleep(3)

        if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
            arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
            print("arg1="+arg1)
            ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
            print("acw_sc__v2="+ACWSCV2)
            acw = requests.cookies.RequestsCookieJar()
            acw.set("acw_sc__v2", ACWSCV2)
            hzmbus.cookies.update(acw)
            continue
        elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
            if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                time.sleep(60)
            continue

        headers["Authorization"] = homepage.json()["jwt"]
        break
    except Exception:
        pass

BUS_STOPS = {
    "ZHO": "珠海",
    "MAC": "澳门",
    "HKG": "香港"
}

# print(homepage.json())

writeLog("[已登录] 主账号完成登陆流程。")"""

mainAccHeaders = {}

hzmbus = None

headers = None

# 主号
while True:
    try:
        hzmbus = requests.Session()

        headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Connection":"keep-alive",
        "Sec-Fetch-Dest":"document",
        "Sec-Fetch-Mode":"navigate",
        "Sec-Fetch-Site":"none",
        "Sec-Fetch-User":"?1",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat",
        "sec-ch-ua": "\"\"", #"\"\"",
        "sec-ch-ua-mobile": "?1", #"?0",
        "sec-ch-ua-platform": "\"\"", #"\"\""
        }

        homepage = hzmbus.get("https://wx.hzmbus.com/wxhtml/", headers=headers)

        # 微信 hzm oauth 数据

        APPID = "wx0257bd1261e4d0f1"

        REDIRECT_URL = "https://wx.hzmbus.com/wxhtml/"

        SCOPE = "snsapi_userinfo"

        STATE = "STATE"

        UIN = input("请输入 uin 参数：")

        VERSION = "6307062c"

        PASS_TICKET = ""

        KEY = ""

        # 微信 hzm oauth 数据


        # 获取 key 和 pass_ticket


        KEY = input("请输入微信登录的 key 参数：")
        PASS_TICKET = input("请输入微信登录的 pass_ticket 参数：")

        # 获取 key 和 pass_ticket

        REDIRECT = parse.quote_plus(REDIRECT_URL)

        PASSTICKET = parse.quote_plus(PASS_TICKET)

        WXOAUTHURL = f"https://open.weixin.qq.com/connect/oauth2/authorize?appid={APPID}&redirect_uri={REDIRECT}&response_type=code&scope={SCOPE}&state={STATE}&uin={UIN}&key={KEY}&version={VERSION}&pass_ticket={PASSTICKET}"

        writeLog("[微信 OAuth] 您的微信 OAuth 链接是：" + WXOAUTHURL)

        homepage = hzmbus.get(WXOAUTHURL, headers=headers)

        UUID = homepage.text.split("name=\"uuid\" value=\"")[1].split("\">")[0]

        oAuthData = {
        "snsapi_userinfo":"on",
        "allow": 1,
        "uuid": UUID,
        "uin": UIN,
        "key": KEY,
        "pass_ticket": PASS_TICKET,
        "version": VERSION
        }

        homepage = hzmbus.post("https://open.weixin.qq.com/connect/oauth2/authorize_reply", headers=headers, data=oAuthData, allow_redirects=False)

        CODE = homepage.headers["Location"].split("?")[1].split("&")[0].split("=")[1]

        writeLog("[微信 code] 您的微信 code 为 " + CODE + " ，该授权码只可用一次。")

        HZM_HOMEPAGE = homepage.headers["Location"]

        homepage = hzmbus.get(HZM_HOMEPAGE, headers=headers)

        HZM_OAUTHLINK = f"https://wx.hzmbus.com/hzmb/wxapi/oauth?code={CODE}"

        headers["Accept"] = "application/json, text/plain, */*"

        while True:
            try:
                homepage = hzmbus.get(HZM_OAUTHLINK, headers=headers)

                writeLog("[登录 OAuth 结果] 登录 OAuth 结果为 " + homepage.json()["messages"])

                break
            except Exception:
                pass

        if homepage.json()["messages"] != "success":
            writeLog("[登录 OAuth 失败] 抱歉！登录 OAuth 失败。")
            continue

        break
    except Exception as e:
        print(e)
        pass

BUS_STOPS = {
    "ZHO": "珠海",
    "MAC": "澳门",
    "HKG": "香港"
}

# print(homepage.json())

mainAccHeaders = headers
mainHzmbus = hzmbus

writeLog("[已登录] 主账号完成登录流程。")

IndexMonitor = 0

time_wait = (61 / (12 * len(info["monitors"])))

MyDones = [False for i in range(len(info["monitors"]))]

MyAllDones = [True for i in range(len(info["monitors"]))]

def LoginToAcc(ACC, IndexMonitor, myHeaders, MyDones):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?1", # "?0",
        "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    hzmbus = requests.Session()

    # writeLog("="*20+"开始运行 (自动选日期)"+"="*20)

    homepage = hzmbus.get("https://i.hzmbus.com/webhtml/login", headers=headers)

    if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
        arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
        print("arg1="+arg1)
        ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
        print("acw_sc__v2="+ACWSCV2)
        acw = requests.cookies.RequestsCookieJar()
        acw.set("acw_sc__v2", ACWSCV2)
        hzmbus.cookies.update(acw)

    hzmbus.get("https://i.hzmbus.com/", headers=headers)
        
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "authorization": "",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\"\"", # "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
        "sec-ch-ua-mobile": "?1", # "?0",
        "sec-ch-ua-platform": "\"\"", # "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": "https://i.hzmbus.com/webhtml/login",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SM-N9860 Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/3171 MMWEBSDK/20211202 Mobile Safari/537.36 MMWEBID/8157 MicroMessenger/8.0.18.2060(0x28001237) Process/toolsmp WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64", #"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }

    while True:
        try:
            homepage = hzmbus.post("https://i.hzmbus.com/webh5api/login", headers=headers, json={
                "webUserid": ACC["uname"],
                "passWord": ACC["pwd"],
                "code":"",
                "appId":"HZMBWEB_HK",
                "joinType":"WEB",
                "version":"2.7.202207.1213",
                "equipment":"PC"
                }, timeout=1);print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))#;time.sleep(3)

            if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                print("arg1="+arg1)
                ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                print("acw_sc__v2="+ACWSCV2)
                acw = requests.cookies.RequestsCookieJar()
                acw.set("acw_sc__v2", ACWSCV2)
                hzmbus.cookies.update(acw)
                continue
            elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                    time.sleep(60)
                continue

            headers["Authorization"] = homepage.json()["jwt"]
            break
        except Exception:
            pass
    
    # print(homepage.json())

    writeLog(f"[已登录] 账号 {IndexMonitor} 完成登陆流程。")

    myHeaders[IndexMonitor] = [hzmbus, headers]
    MyDones[IndexMonitor] = True

myThreads = []
for i in range(len(info["monitors"])):
    myT = threading.Thread(target = LoginToAcc, args = (info["monitors"][i], i, myHeaders, MyDones))
    myT.start()

while MyDones != MyAllDones:
    pass

ROUTE = info["route"]

TRACK = info.get("track", "")

START = ROUTE[:3]

END = ROUTE[3:]

PASSENGERS = info["passengers"]

ADULTS = 0
KIDS = 0

for PASSENGER in PASSENGERS:
    if PASSENGER["ticketType"] == "00":
        ADULTS += 1
    elif PASSENGER["ticketType"] == "01":
        KIDS += 1

# TODO: 在这里添加 等到 8:00 PM

TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

#get time by using taobao api，这一行之前的代码需要在10点前幾分鐘执行
#from urllib import request
#from urllib.request import Request,urlopen

eightPM = 20

#myFinal = ""
#head={
#    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, #like Gecko) Chrome/98.0.4758.80 Safari/537.36' 
#}
#url1="https://worldtimeapi.org/api/timezone/Asia/Shanghai"
#r=Request(url1)
#js=urlopen(r)
#data=js.read()
#data=str(data)
#time3=data[249:252]
#dt=int()/1000-time.time()
#print(dt)
DF = "%Y-%m-%d"
oldtime_wait = 0.01
FINISHEDCAPTCHA = False
my_cap = {"sessionId": "", "sig": "", "token": ""}
writeLog("[提示] 等待中...")
while True:
    #timeArray=time.localtime(time.time()+dt)
    #jsTime=time.strftime("%Y-%m-%d %H:%M:%S")
    #nowTime=jsTime[11:19]
    #hour=int(nowTime.split(":")[0])
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()
    # writeLog("[时间] 目前时间为" + str(now.hour * 3600 + now.minute * 60 + now.second))
    if ((weekday == 1 and (now.hour * 3600 + now.minute * 60 + now.second >= 71700 and now.hour * 3600 + now.minute * 60 + now.second <= 77400)) and not FINISHEDCAPTCHA):
        CAPTCHA = 2
        writeLog("[滑块时间] 滑块时间到。")
        if CAPTCHA == 2:
            TIMESHUA = True
            oldtime_wait = time_wait
            time_wait = 0.01
            FINISHEDCAPTCHA = True
            referrerURL = f"https://i.hzmbus.com/webhtml/ticket_details?xlmc_1={BUS_STOPS[START]}&xlmc_2={BUS_STOPS[END]}&xllb=1&xldm={ROUTE}&code_1={START}&code_2={END}"
            referrerURL = parse.quote_plus(referrerURL)
            my_cap = crack_ali.slide(hzmbus, headers, referrerURL, "FFFF0N0000000000A95D", "nc_other_h5", "6748c822ee91e", TRACK)
            if my_cap == None:
                break
    elif not (weekday == 1 and (now.hour * 3600 + now.minute * 60 + now.second >= 71460 and now.hour * 3600 + now.minute * 60 + now.second <= 77400)):
        CAPTCHA = 1
    if (weekday != 1) or (hour >= eightPM):
        if CAPTCHA == 1:
            my_cap = {"sessionId": "", "sig": "", "token": ""}
        while True:
            gotTicket = False
            while not gotTicket:
                DATE_CHECKER = datetime.datetime.now()
                bestTiming = None
                numPeople = None
                lastNumPeople = None
                bestDate = None
                bestBestTiming = None
                DAYS_UNTIL_NEXT_TUESDAY = datetime.timedelta( (1-datetime.datetime.today().weekday()) % 7 ).days
                if DAYS_UNTIL_NEXT_TUESDAY == 0:
                    DAYS_UNTIL_NEXT_TUESDAY = 7
                DAYS_UNTIL_NEXT_TUESDAY += 5
                NEXTMONDAY = DATE_CHECKER + datetime.timedelta(days=(DAYS_UNTIL_NEXT_TUESDAY - 6))
                if NEXTMONDAY >= DATE_CHECKER and DATE_CHECKER.weekday() == 1:
                    DATE_CHECKER = NEXTMONDAY
                    DAYS_UNTIL_NEXT_TUESDAY = 6
                writeLog("[监控] 您有 " + str(len(info["monitors"])) + " 个账号，每次刷票约需等 " + str(int(time_wait * DAYS_UNTIL_NEXT_TUESDAY * 1)) + " 秒。")
                day = 0
                accNum = 0
                while True:
                    myC = False
                    if rateLimited[accNum] != None:
                        if time.time() - rateLimited[accNum] <= 60:
                            # writeLog(f"[已限速] 账号 {accNum} 已被限速。")
                            accNum += 1
                            accNum = accNum % len(myHeaders)
                            continue
                        else:
                            rateLimited[accNum] = None
                    hzmbus = myHeaders[accNum][0]
                    headers = myHeaders[accNum][1]
                    writeLog(f"[查询] 正在使用账号 {accNum} 查询余票。")
                    if day > DAYS_UNTIL_NEXT_TUESDAY:
                        break
                    DATE = DATE_CHECKER.strftime(DF)
                    writeLog(f"[购票中] 正在购买 日期 {DATE}，从 {BUS_STOPS[START]} => 往 {BUS_STOPS[END]} 车次的车票。")
                    """while True:
                        try:
                            homepage = hzmbus.post("https://i.hzmbus.com/webh5api/ticket/query.line.ticket.price", headers=headers, json={
                                "buyDate":DATE,
                                "lineCode":ROUTE,
                                "appId":"HZMBWEB_HK",
                                "joinType":"WEB",
                                "version":"2.7.202207.1213",
                                "equipment":"PC"
                            });print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                            #time.sleep(time_wait)
                            if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                                arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                                print("arg1="+arg1)
                                ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                                print("acw_sc__v2="+ACWSCV2)
                                acw = requests.cookies.RequestsCookieJar()
                                acw.set("acw_sc__v2", ACWSCV2)
                                hzmbus.cookies.update(acw)
                                continue
                            if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                                rateLimited[accNum] = None
                            elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")) and checkAll():
                                    time.sleep(60)
                                elif ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                    rateLimited[accNum] = time.time()
                                    accNum += 1
                                    accNum = accNum % len(myHeaders)
                                myC = True
                                break
                            if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                                writeLog("[被限速] 要等一会儿。")
                                # time.sleep(30*60) # 等 30 分
                                continue
                            homepage.json()
                            break
                        except Exception:
                            continue
                    
                    if myC:
                        continue

                    PRICES = homepage.json()"""

                    ADULT_PRICE = 65 # PRICES["responseData"][0]["adultHKD"]
                    KID_PRICE = 33 # PRICES["responseData"][0]["childrenHKD"]

                    TOTAL_PRICE = (ADULTS * ADULT_PRICE) + (KIDS * KID_PRICE)

                    TOTAL_PRICE = int(TOTAL_PRICE)

                    while True:
                        try:
                            homepage = hzmbus.post("https://i.hzmbus.com/webh5api/manage/query.book.info.data", headers=headers, json={
                                "bookDate":DATE,
                                "lineCode":ROUTE,
                                "appId":"HZMBWEB_HK",
                                "joinType":"WEB",
                                "version":"2.7.202207.1213",
                                "equipment":"PC"
                            });print("[请求结果] 该次请求结果为 " + str(homepage.content, encoding="UTF-8"))
                            time.sleep(time_wait)
                            if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                                arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                                print("arg1="+arg1)
                                ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                                print("acw_sc__v2="+ACWSCV2)
                                acw = requests.cookies.RequestsCookieJar()
                                acw.set("acw_sc__v2", ACWSCV2)
                                hzmbus.cookies.update(acw)
                                continue
                            if "操作频繁" not in str(homepage.content, encoding="UTF-8"):
                                rateLimited[accNum] = None
                            elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")) and (checkAll()):
                                    time.sleep(60)
                                elif ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                    myC = True
                                    rateLimited[accNum] = time.time()
                                    accNum += 1
                                    accNum = accNum % len(myHeaders)
                                if ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")):
                                    continue
                                break
                            if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                                writeLog("[被限速] 要等一会儿。")
                                # time.sleep(30*60) # 等 30 分
                                continue
                            homepage.json()
                            break
                        except Exception:
                            continue

                    if myC:
                        continue

                    TIMES = homepage.json()["responseData"]

                    bestTiming = None
                    numPeople = None


                    for TIME in TIMES:
                        if bestTiming == None and numPeople == None:
                            print(TIME)
                            bestTiming = TIME.get("beginTime", "00:00:00")
                            numPeople = TIME.get("maxPeople", 0)
                            if numPeople >= len(PASSENGERS):
                                lastNumPeople = numPeople
                                bestDate = DATE
                                bestBestTiming = bestTiming
                                gotTicket = True
                                break
                        else:
                            if TIME.get("maxPeople", 0) > numPeople:
                                bestTiming = TIME.get("beginTime", "00:00:00")
                                numPeople = TIME.get("maxPeople", 0)
                            if numPeople >= len(PASSENGERS):
                                lastNumPeople = numPeople
                                bestDate = DATE
                                bestBestTiming = bestTiming
                                gotTicket = True
                                break

                    #检查 乘客数量

                    if numPeople <= 0:
                        writeLog("[没有空位] 抱歉！没有空位。")
                        # time.sleep(5 * 60)
                        # continue

                    if numPeople < len(PASSENGERS) and numPeople > 0:
                        writeLog("[位置不够] 抱歉！可用票额不可容下您的同住人。")
                        # continue

                    if (lastNumPeople != None and bestDate != None):
                        if numPeople > lastNumPeople: # 第 >=2 日。
                            lastNumPeople = numPeople
                            bestDate = DATE
                            bestBestTiming = bestTiming
                    elif (lastNumPeople == None and bestDate == None) and numPeople != None: # First day. 第一日。
                        lastNumPeople = numPeople
                        bestDate = DATE
                        bestBestTiming = bestTiming

                    if lastNumPeople >= len(PASSENGERS):
                        break
                    day += 1
                    # accNum += 1
                    # accNum = accNum % len(myHeaders)
                    DATE_CHECKER += datetime.timedelta(days=1)
                if lastNumPeople == 0 or lastNumPeople < len(PASSENGERS):
                    writeLog("[抱歉] 暂无可用日期。")
                    # break
                else:
                    writeLog(f"[有票] 找到 {bestDate} {bestBestTiming} 班次的车票。")
                    gotTicket = True
            if TIMESHUA:
                TIMESHUA = False
                time_wait = oldtime_wait
                oldtime_wait = 0.01
            DATE = bestDate
            bestTiming = bestBestTiming
            headers = mainAccHeaders
            hzmbus = mainHzmbus
            while True:
                if CAPTCHA == 1:
                    result = None

                    while result == None:
                        homepage = hzmbus.get("https://i.hzmbus.com/webh5api/captcha", headers=headers)
                        try:
                            if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                                arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                                print("arg1="+arg1)
                                ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                                print("acw_sc__v2="+ACWSCV2)
                                acw = requests.cookies.RequestsCookieJar()
                                acw.set("acw_sc__v2", ACWSCV2)
                                hzmbus.cookies.update(acw)
                                result = None
                                continue
                            elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                result = None
                                if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                    time.sleep(60)
                                continue
                        except Exception:
                            pass

                        with open("captcha_buy.png", "wb") as code:
                            code.write(homepage.content)

                        recognizer = ddddocr.DdddOcr()

                        code = open("captcha_buy.png", "rb").read()

                        result = recognizer.classification(code)

                        if not (result.isnumeric() and len(result) == 4):

                            writeLog("[验证码失败] 哎哟！我没有识别正确。")

                            result = None

                    writeLog("[验证码结果] 验证码结果为 " + result)
                elif CWRONG:
                    result = ""
                    TIMESHUA = True
                    oldtime_wait = time_wait
                    time_wait = 0.01
                    FINISHEDCAPTCHA = True
                    referrerURL = f"https://i.hzmbus.com/webhtml/ticket_details?xlmc_1={BUS_STOPS[START]}&xlmc_2={BUS_STOPS[END]}&xllb=1&xldm={ROUTE}&code_1={START}&code_2={END}"
                    referrerURL = parse.quote_plus(referrerURL)
                    my_cap = crack_ali.slide(hzmbus, headers, referrerURL, "FFFF0N0000000000A95D", "nc_other_h5", "6748c822ee91e", TRACK)
                    if my_cap == None:
                        break
                if CAPTCHA == 2:
                    result = ""
                while True:
                    try:
                        homepage = hzmbus.post("https://wx.hzmbus.com/webapi/ticket/buy.ticket", headers=headers, json={
                        "ticketData": DATE,
                        "lineCode": ROUTE,
                        "startStationCode": START,
                        "endStationCode": END,
                        "boardingPointCode": START + "01",
                        "breakoutPointCode": END + "01",
                        "currency": "2",
                        "ticketCategory": "1",
                        "tickets": PASSENGERS,
                        "amount": TOTAL_PRICE * 100,
                        "feeType": 9,
                        "totalVoucherpay": 0,
                        "voucherNum": 0,
                        "voucherStr": "",
                        "totalBalpay": 0,
                        "totalNeedpay": TOTAL_PRICE * 100,
                        "bookBeginTime": bestTiming,
                        "bookEndTime": bestTiming,
                        "captcha": result,
                        "sessionId": "" if CAPTCHA == 1 else my_cap["sessionId"],
                        "sig": "" if CAPTCHA == 1 else my_cap["sig"],
                        "token": "" if CAPTCHA == 1 else my_cap["token"],
                        "timestamp": int(time.time()),
                        "appId": "HZMBWEB_HK",
                        "joinType": "WEB",
                        "version": "2.7.202207.1213",
                        "equipment": "PC"
                        }, timeout=5)
                        if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                            arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                            print("arg1="+arg1)
                            ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                            print("acw_sc__v2="+ACWSCV2)
                            acw = requests.cookies.RequestsCookieJar()
                            acw.set("acw_sc__v2", ACWSCV2)
                            hzmbus.cookies.update(acw)
                            continue
                        elif ("系统异常" in str(homepage.content, encoding="UTF-8") or "系统繁忙" in str(homepage.content, encoding="UTF-8")) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                            if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                time.sleep(60)
                            continue
                        homepage.json()
                        break
                    except Exception as e:
                        print(e)
                        pass

                writeLog("[购票结果] 购票结果为 " + str(homepage.content, encoding="UTF-8"))

                if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                    print("arg1="+arg1)
                    ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                    print("acw_sc__v2="+ACWSCV2)
                    acw = requests.cookies.RequestsCookieJar()
                    acw.set("acw_sc__v2", ACWSCV2)
                    hzmbus.cookies.update(acw)
                    continue

                SUCCESS = homepage.json().get("code", "FAILURE") == "SUCCESS"

                if SUCCESS:
                    writeLog("[购票成功] 请抓紧时间支付车费。")
                    ticket_success(hzmbus, headers, homepage.json()["responseData"]["orderNumber"], homepage.json()["responseData"]["orderReqno"]) # ticket_success()
                    break
                else:
                    if homepage.json().get("message", "无信息") == "验证码不能为空" and CAPTCHA == 2:
                        writeLog("[图形验证] 验证码类型预测错误。")
                        CAPTCHA = 1
                        continue
                    if homepage.json().get("message", "无信息") == "验证码不正确" or "会话ID" in homepage.json().get("message", "无信息"):
                        if "会话ID" in homepage.json().get("message", "无信息") and CAPTCHA == 1:
                            CAPTCHA = 2
                            writeLog("[滑块验证] 验证码类型预测错误。")
                            CWRONG = True
                            continue
                        writeLog("[哎呀] 没能够搞定验证码。");time.sleep(1)
                        continue
                    if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                        writeLog("[被限速] 要等一会儿。")
                        # time.sleep(30*60) # 等 30 分
                        continue
                    writeLog("[购票失败] 抱歉！购票流程中出现问题。")
                    ticket_failure()
                    break

            break

            # 流程完毕后， 提示用户给钱。票源会留着，别担心。
        break
