import requests
import time
import sys
import datetime
import ddddocr
import json
import smtplib
import hzmbus_hash;import crack_ali
import acw_sc_v2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from urllib import parse

# 00 = 成人 , 01 = 儿童
# 请使用港币支付
# 需要于 8：00 前几分钟运行。

CAPTCHA = 2 # 2 = 阿里云， 1 = 文字

info = json.loads(open("info.json", "r").read());myURL = "https://wx.hzmbus.com/wxhtml/index.html"

def ticket_success():
    global info
    print("Bought ticket")
    myDates = info["date"]
    myEmailContent = open("HZMB_Success_Email.html", "r", encoding="UTF-8").read()
    myEmailContent = myEmailContent.replace("[INSERT DATES HERE]", myDates)
    myEmailTContent = open("HZMB_Success_Email.txt", "r", encoding="UTF-8").read()
    myEmailTContent = myEmailTContent.replace("[INSERT DATES HERE]", myDates)
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
  log = open("log.txt", "a", encoding="UTF-8")
  myLog = (_text+"\n")
  log.write(myLog)
  log.close()

writeLog("="*20+"开始运行"+"="*20)

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

writeLog("[已登录] 完成登陆流程。")

ROUTE = info["route"]

TRACK = info.get("track", "")

START = ROUTE[:3]

END = ROUTE[3:]

DATE = info["date"]

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
FINISHEDCAPTCHA = False
my_cap = {"sessionId": "", "sig": "", "token": ""};myhash = hzmbus_hash.HZMHash()
writeLog("[提示] 等待中...")
while True:
    #timeArray=time.localtime(time.time()+dt)
    #jsTime=time.strftime("%Y-%m-%d %H:%M:%S")
    #nowTime=jsTime[11:19]
    #hour=int(nowTime.split(":")[0])
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()
    writeLog("[时间] 目前时间为" + now.strftime(TIMEFORMAT))
    if (weekday != 1) or (hour >= eightPM):
        if CAPTCHA == 1:
            my_cap = {"sessionId": "", "sig": "", "token": ""};myhash = hzmbus_hash.HZMHash()
        while True:
            writeLog(f"[购票中] 正在购买 {BUS_STOPS[START]} => {BUS_STOPS[END]} 车次的车票。")
            while True:
                try:
                    homepage = hzmbus.post("https://wx.hzmbus.com/webapi/ticket/query.line.ticket.price", headers=headers, json={
                        "buyDate":DATE,
                        "lineCode":ROUTE,
                        "appId":"HZMBWEB_HK",
                        "joinType":"WEB",
                        "version":"2.7.202207.1213",
                        "equipment":"PC"
                    });print(str(homepage.content, encoding="UTF-8"))

                    if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                        arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                        print("arg1="+arg1)
                        ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                        print("acw_sc__v2="+ACWSCV2)
                        acw = requests.cookies.RequestsCookieJar()
                        acw.set("acw_sc__v2", ACWSCV2)
                        hzmbus.cookies.update(acw)
                        continue
                    if ("系统异常" in str(homepage.content, encoding="UTF-8") or ("系统繁忙" in str(homepage.content, encoding="UTF-8") or "系統繁忙" in str(homepage.content, encoding="UTF-8"))) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                        if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                            time.sleep(60)
                        continue
                    homepage.json()
                    break
                except Exception:
                    continue

            PRICES = homepage.json()

            if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                writeLog("[被限速] 要等一会儿。")
                # time.sleep(30*60) # 等 30 分
                continue     

            ADULT_PRICE = PRICES["responseData"][0]["adultCNY"]
            KID_PRICE = PRICES["responseData"][0]["childrenCNY"]

            TOTAL_PRICE = (ADULTS * ADULT_PRICE) + (KIDS * KID_PRICE)

            TOTAL_PRICE = int(TOTAL_PRICE)

            bestTiming = info["time"]

            while True:
                if CAPTCHA == 1:
                    result = None

                    while result == None:
                        homepage = hzmbus.get("https://wx.hzmbus.com/hzmb/webapi/captcha", headers=headers)

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
                            if ("系统异常" in str(homepage.content, encoding="UTF-8") or ("系统繁忙" in str(homepage.content, encoding="UTF-8") or "系統繁忙" in str(homepage.content, encoding="UTF-8"))) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                    time.sleep(60)
                                continue
                        except Exception:
                            pass
                        
                        with open("captcha_buy.png", "wb") as code:
                            code.write(homepage.content)

                        recognizer = ddddocr.DdddOcr(old=True)

                        code = open("captcha_buy.png", "rb").read()

                        result = recognizer.classification(code)


                        if not (result.isnumeric() and len(result) == 4):

                            writeLog("[验证码失败] 哎哟！我没有识别正确。")

                            result = None

                    writeLog("[验证码结果] 验证码结果为 " + result)
                else:
                    result = ""
                    if CAPTCHA == 2:
                        FINISHEDCAPTCHA = True
                        referrerURL = f"https://i.hzmbus.com/webhtml/ticket_details?xlmc_1={BUS_STOPS[START]}&xlmc_2={BUS_STOPS[END]}&xllb=1&xldm={ROUTE}&code_1={START}&code_2={END}"
                        referrerURL = parse.quote_plus(referrerURL)
                        myhash.activate_browser(url=myURL, disable_redirects=True);my_cap = crack_ali.slide(hzmbus, headers, referrerURL, "FFFF0N0000000000A95D", "nc_other_h5", "6748c822ee91e", TRACK)
                        if my_cap == None:
                            break
                while True:
                    try:
                        homepage = hzmbus.post("https://wx.hzmbus.com/webapi/ticket/buy.ticket", headers=headers, json=myhash.set_token_web({
                        "ticketData": DATE,
                        "lineCode": ROUTE,
                        "startStationCode": START,
                        "endStationCode": END,
                        "boardingPointCode": START + "01",
                        "breakoutPointCode": END + "01",
                        "currency": "1",
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
                        "timestamp": int(time.time())
                        }), timeout=5)
                        if str(homepage.content, encoding="UTF-8").startswith("<html><script>"):
                            arg1 = acw_sc_v2.getArg1FromHTML(str(homepage.content, encoding="UTF-8"))
                            print("arg1="+arg1)
                            ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                            print("acw_sc__v2="+ACWSCV2)
                            acw = requests.cookies.RequestsCookieJar()
                            acw.set("acw_sc__v2", ACWSCV2)
                            hzmbus.cookies.update(acw)
                            continue
                        if ("系统异常" in str(homepage.content, encoding="UTF-8") or ("系统繁忙" in str(homepage.content, encoding="UTF-8") or "系統繁忙" in str(homepage.content, encoding="UTF-8"))) or ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                            if ("操作频繁" in str(homepage.content, encoding="UTF-8") or "DTD HTML 2.0" in str(homepage.content, encoding="UTF-8")):
                                time.sleep(60)
                            continue
                        homepage.json()
                        break
                    except Exception as e:
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
                    ticket_success()
                    break
                else:
                    if homepage.json().get("message", "无信息") == "验证码不正确" or "会话ID" in homepage.json().get("message", "无信息"):
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