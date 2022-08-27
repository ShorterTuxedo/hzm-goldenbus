import requests
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

# 00 = 成人 , 01 = 儿童
# 请使用港币支付
# 需要于 8：00 前几分钟运行。

CAPTCHA = 2 # 2 = 阿里云， 1 = 文字

info = json.loads(open("info.json", "r").read())

DATE = "1970-01-01" # 替代日期

def ticket_success():
    global DATE
    print("Bought ticket")
    myDates = DATE
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

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-language": "zh-CN,zh;q=0.9",
    "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
  }

hzmbus = requests.Session()

writeLog("="*20+"开始运行 (自动选日期)"+"="*20)

homepage = hzmbus.get("https://i.hzmbus.com/webhtml/login", headers=headers)

if homepage.text.startswith("<html><script>"):
    arg1 = acw_sc_v2.getArg1FromHTML(homepage.text)
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
    "sec-ch-ua": "\".Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"103\", \"Chromium\";v=\"103\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Referer": "https://i.hzmbus.com/webhtml/login",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}

homepage = hzmbus.post("https://i.hzmbus.com/webh5api/login", headers=headers, json={
    "webUserid": info["uname"],
    "passWord": info["pwd"],
    "code":"",
    "appId":"HZMBWEB_HK",
    "joinType":"WEB",
    "version":"2.7.202207.1213",
    "equipment":"PC"
    })

BUS_STOPS = {
    "ZHO": "珠海",
    "MAC": "澳门",
    "HKG": "香港"
}

# print(homepage.json())

headers["Authorization"] = homepage.json()["jwt"]

writeLog("[已登录] 完成登陆流程。")

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
FINISHEDCAPTCHA = False
writeLog("[提示] 等待中...")
while True:
    #timeArray=time.localtime(time.time()+dt)
    #jsTime=time.strftime("%Y-%m-%d %H:%M:%S")
    #nowTime=jsTime[11:19]
    #hour=int(nowTime.split(":")[0])
    now = datetime.datetime.now()
    hour = now.hour
    weekday = now.weekday()
    my_cap = {"sessionId": "", "sig": "", "token": ""}
    writeLog("[时间] 目前时间为" + now.strftime(TIMEFORMAT))
    if (not FINISHEDCAPTCHA) and (((weekday == 1) and (now.hour == 19 and (now.minute >= 50 and now.minute <= 59))) and CAPTCHA == 2):
        FINISHEDCAPTCHA = True
        referrerURL = f"https://i.hzmbus.com/webhtml/ticket_details?xlmc_1={BUS_STOPS[START]}&xlmc_2={BUS_STOPS[END]}&xllb=1&xldm={ROUTE}&code_1={START}&code_2={END}"
        referrerURL = parse.quote_plus(referrerURL)
        my_cap = crack_ali.slide(hzmbus, headers, referrerURL, "FFFF0N0000000000A95D", "nc_other_h5", "6748c822ee91e", TRACK)
        if my_cap == None:
            break
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
                day = 0
                while True:
                    if day > DAYS_UNTIL_NEXT_TUESDAY:
                        break
                    DATE = DATE_CHECKER.strftime(DF)
                    writeLog(f"[购票中] 正在购买 日期 {DATE}，从 {BUS_STOPS[START]} => 往 {BUS_STOPS[END]} 车次的车票。")
                    homepage = hzmbus.post("https://i.hzmbus.com/webh5api/ticket/query.line.ticket.price", headers=headers, json={
                        "buyDate":DATE,
                        "lineCode":ROUTE,
                        "appId":"HZMBWEB_HK",
                        "joinType":"WEB",
                        "version":"2.7.202207.1213",
                        "equipment":"PC"
                    })
                    if homepage.text.startswith("<html><script>"):
                        arg1 = acw_sc_v2.getArg1FromHTML(homepage.text)
                        print("arg1="+arg1)
                        ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                        print("acw_sc__v2="+ACWSCV2)
                        acw = requests.cookies.RequestsCookieJar()
                        acw.set("acw_sc__v2", ACWSCV2)
                        hzmbus.cookies.update(acw)
                        continue
                    if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                        writeLog("[被限速] 要等一会儿。")
                        # time.sleep(30*60) # 等 30 分
                        continue
                    
                    PRICES = homepage.json()

                    ADULT_PRICE = PRICES["responseData"][0]["adultHKD"]
                    KID_PRICE = PRICES["responseData"][0]["childrenHKD"]

                    TOTAL_PRICE = (ADULTS * ADULT_PRICE) + (KIDS * KID_PRICE)

                    TOTAL_PRICE = int(TOTAL_PRICE)

                    homepage = hzmbus.post("https://i.hzmbus.com/webh5api/manage/query.book.info.data", headers=headers, json={
                        "bookDate":DATE,
                        "lineCode":ROUTE,
                        "appId":"HZMBWEB_HK",
                        "joinType":"WEB",
                        "version":"2.7.202207.1213",
                        "equipment":"PC"
                    })
                    if homepage.text.startswith("<html><script>"):
                        arg1 = acw_sc_v2.getArg1FromHTML(homepage.text)
                        print("arg1="+arg1)
                        ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                        print("acw_sc__v2="+ACWSCV2)
                        acw = requests.cookies.RequestsCookieJar()
                        acw.set("acw_sc__v2", ACWSCV2)
                        hzmbus.cookies.update(acw)
                        continue
                    if homepage.json().get("message", "无信息") == "操作频繁,请稍后再试":
                        writeLog("[被限速] 要等一会儿。")
                        # time.sleep(30*60) # 等 30 分
                        continue

                    TIMES = homepage.json()["responseData"]

                    bestTiming = None
                    numPeople = None


                    for TIME in TIMES:
                        if bestTiming == None and numPeople == None:
                            print(TIME)
                            bestTiming = TIME.get("beginTime", "00:00:00")
                            numPeople = TIME.get("maxPeople", 0)
                        else:
                            if TIME.get("maxPeople", 0) < numPeople:
                                bestTiming = TIME.get("beginTime", "00:00:00")
                                numPeople = TIME.get("maxPeople", 0)

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
                    day += 1
                    DATE_CHECKER += datetime.timedelta(days=1)
                if lastNumPeople == 0:
                    writeLog("[抱歉] 暂无可用日期。")
                    # break
                else:
                    writeLog(f"[有票] 找到 {bestDate} {bestBestTiming} 车次的车票。")
                    gotTicket = True
            DATE = bestDate
            bestTiming = bestBestTiming
            while True:
                if CAPTCHA == 1:
                    result = None

                    while result == None:
                        homepage = hzmbus.get("https://i.hzmbus.com/webh5api/captcha", headers=headers)

                        try:
                            if homepage.text.startswith("<html><script>"):
                                arg1 = acw_sc_v2.getArg1FromHTML(homepage.text)
                                print("arg1="+arg1)
                                ACWSCV2 = acw_sc_v2.getAcwScV2(arg1)
                                print("acw_sc__v2="+ACWSCV2)
                                acw = requests.cookies.RequestsCookieJar()
                                acw.set("acw_sc__v2", ACWSCV2)
                                hzmbus.cookies.update(acw)
                                result = None
                                continue
                        except Exception:
                            pass

                        with open("captcha_buy.png", "wb") as code:
                            code.write(homepage.content)

                        recognizer = ddddocr.DdddOcr(old=True)

                        code = open("captcha_buy.png", "rb").read()

                        result = recognizer.classification(code)

                        if not result.isnumeric():

                            writeLog("[验证码失败] 哎哟！我没有识别正确。")

                            result = None

                    writeLog("[验证码结果] 验证码结果为 " + result)
                else:
                    result = ""

                homepage = hzmbus.post("https://i.hzmbus.com/webh5api/ticket/buy.ticket", headers=headers, json={
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
                })

                writeLog("[购票结果] 购票结果为 " + str(homepage.content, encoding="UTF-8"))

                if homepage.text.startswith("<html><script>"):
                    arg1 = acw_sc_v2.getArg1FromHTML(homepage.text)
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
                    if homepage.json().get("message", "无信息") == "验证码不正确":
                        writeLog("[哎呀] 没能够搞定验证码。")
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
