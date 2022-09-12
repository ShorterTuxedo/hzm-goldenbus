import os
import json


info = {}

def clearScreen():
    print(str(os.system("cls" if os.system == "nt" else "clear"))[0:0], end="")

ROUTES1 = {
    "香港 -> 珠海": "HKGZHO",
    "珠海 -> 香港": "ZHOHKG",
    "香港 -> 澳门": "HKGMAC",
    "澳门 -> 香港": "MACHKG"
}

ROUTES2 = {
    "HKGZHO": "香港 -> 珠海",
    "ZHOHKG": "珠海 -> 香港",
    "HKGMAC": "香港 -> 澳门",
    "MACHKG": "澳门 -> 香港"
}

def validate_email(email):
    if "@" in email and "." in email:
        return True
    return False

def validate_date(date_):
    date = str(date_)
    if len(date) == 10:
        for char in date:
            if (not char in "1234567890-"):
                return False
        if len(date.split("-")) == 3 and (date[4] == "-" and date[7] == "-"):
            return True
        else:
            return False
    else:
        return False

def validate_time(time_):
    time = time_
    if len(time) != 8:
        return False
    else:
        try:
            if len(time.split(":")) == 3 and (((int(time.split(":")[0]) >= 0 and int(time.split(":")[0]) < 24) and (int(time.split(":")[1]) >= 0 and int(time.split(":")[1]) < 59)) and (int(time.split(":")[2]) >= 0 and int(time.split(":")[2]) < 59)):
                return True
        except Exception:
            return False

buyers = []
route = ""
date = ""
passengers = []
mysendemail = ""
emailreceivers = []
smtppwd = ""
smtphost = ""
smtpport = None
time_ =  None
myChoice = None
track = ""
monitors = []
autopay = False

while myChoice != "7":
    clearScreen()
    print("="*20+"金 巴 抢 票 机 器 人 设 置 主 菜 单"+"="*20+'''
    0. 从 文 件 导 入
    1. 显 示 信 息
    2. 添 加 乘 客 （ 同 行 人 ）
    3. 设 置 购 票 账 号 登 录 信 息
    4. 设 置 SMTP 信 息 和 电 邮 接 收 人
    5. 设 置 出 发 日 期
    6. 设 置 路 线
    7. 保 存 并 退 出
    8. 设 置 出 发 时 间
    9. 输 入 轨 迹
    10. 添 加 余 票 账 号
    11. 设 置 支 付 电 邮
    
    请 输 入 您 的 选 择：''', end="")
    myChoice = input()
    if myChoice == "0":
        clearScreen()
        print("="*20 + "从 文 件 导 入" + "="*20)
        try:
            info = json.loads(open("info.json", "r").read())
            buyers = info.get("buyers", [])
            date = info["date"]
            route = info["route"]
            passengers = info["passengers"]
            mysendemail = info["mysendemail"]
            emailreceivers = info["emailreceivers"]
            smtphost = info["smtphost"]
            smtpport = info["smtpport"]
            smtppwd = info["smtppwd"]
            track = info.get("track", "")
            autopay = info.get("autopay", False)
            monitors = info.get("monitors", [])
            print("        文 件 导 入 成 功！")
            input("按 【 回 车 】 键 返 回 ...")
        except Exception:
            print("        文 件 导 入 失 败！")
            input("按 【 回 车 】 键 返 回 ...")
    if myChoice == "1":
        clearScreen()
        route2 = "暂 无" if route == "" else ROUTES2[route]
        date2 = "暂 无" if (not validate_date(date)) else date
        time_2 = "暂 无" if time_ == None else time_
        passengers2 = "暂 无"
        if len(passengers) > 0:
            passengers2 = "\n"
            for passenger in passengers:
                passengers2 += "        "
                passengers2 += passenger["userName"] + "    "
                passengers2 += passenger["idCard"] + "    "
                if passenger["ticketType"] == "00":
                    passengers2 += " （成 人 票）"
                elif passenger["ticketType"] == "01":
                    passengers2 += " （优 惠 票）"
                passengers2 += "\n"
        monitors2 = "暂 无"
        if len(monitors) > 0:
            monitors2 = "\n"
            for monitor in monitors:
                monitors2 += "        账 号 资 料：    用户名："
                monitors2 += monitor["uname"] + "    密码："
                monitors2 += monitor["pwd"]
                monitors2 += "\n"
        buyers2 = "暂 无"
        if len(buyers) > 0:
            buyers2 = "\n"
            for buyer in buyers:
                buyers2 += "        账 号 资 料：    用户名："
                buyers2 += monitor["uname"] + "    密码："
                buyers2 += monitor["pwd"]
                buyers2 += "\n"
        mysendemail2 = "暂 无" if (not validate_email(mysendemail)) else mysendemail
        emailreceivers2 = emailreceivers
        for i in range(len(emailreceivers2)):
            if not validate_email(emailreceivers2[i]):
                emailreceivers2[i] == "暂 无"
        emailreceivers2 = "，".join(emailreceivers2)
        emailreceivers2 = "暂 无" if emailreceivers2 == "" else emailreceivers2
        smtppwd2 = "暂 无" if smtppwd == "" else smtppwd
        smtphost2 = "暂 无" if smtphost == "" else smtphost
        smtpport2 = "暂 无" if smtpport == None else smtpport
        track2 = "暂 无" if track == "" else track
        autopay2 = "是" if autopay else "否"
        print("="*20+"信 息" + "="*20+f'''
        请 确 认 以 下 所 有 信 息 完 全 正 确 无 误 ，
        否 则 可 能 无 法 购 票 / 被 拒 登 车 ！

        购 票 账 号：{buyers2}
        金 巴 路 线：{route2}
        出 发 日 期：{date2}
        出 发 时 间：{time_2}
        金 巴 乘 客：{passengers2}
        SMTP 发 送 电 邮：{mysendemail2}
        SMTP 接 收 人 电 邮：{emailreceivers2}
        SMTP 密 码：{smtppwd2}
        SMTP 端 口：{smtpport2}
        验 证 码 轨 迹：{track2}
        余 票 账 号：{monitors2}
        支 付 电 邮 开 启： {autopay2}
        ''')
        input("按 【 回 车 】 键 返 回 ...")
    if myChoice == "2":
        clearScreen()
        print("="*20 + "添 加 乘 客 （同 行 人）" + "="*20)
        ticketType = None
        while ticketType == None:
            ticketType = input('''
        请 输 入 乘 客 年 龄。
        （00） ： 成 人
        （01） ： 儿 童 / 长 者
        请 输 入 您 的 选 择：''')
            if ticketType != "00" and ticketType != "01":
                ticketType = None
        userName = None
        while userName == None:
            userName = input('''        请 输 入 乘 客 名 称：''')
        idCard = None
        while idCard == None:
            idCard = input('''        请 输 入 乘 客 证 件 号 码：''')
        passengers.append({
          "ticketType": ticketType,
          "idCard": idCard,
          "idType": 1,
          "userName": userName,
          "telNum": ""
        })
    if myChoice == "6":
        myRouteChosen = None
        while myRouteChosen == None:
            try:
                clearScreen()
                print("="*20 + "设 置 路 线" + "="*20)
                myRoutes = list(range(1, len(list(ROUTES1.keys()))+1))
                # print(myRoutes)
                print("        请 选 择 路 线：")
                for routeIndex in myRoutes:
                    myRoute = list(ROUTES1.keys())[routeIndex-1]
                    print(f"        {routeIndex}.    {myRoute}")
                route = int(input("        请 输 入 您 的 选 择："))
                if (not route in myRoutes):
                    myRouteChosen = None
                else:
                    myRouteChosen = ROUTES1[list(ROUTES1.keys())[route-1]]
            except Exception:
                myRouteChosen = None
        route = myRouteChosen
    if myChoice == "3":
        clearScreen()
        print("="*20+"设 置 购 票 账 号 登 录 信 息" + "="*20)
        unam = None
        while unam == None:
            unam = input("        请 输 入 金 巴 登 录 电 邮：")
            if not validate_email(unam):
                unam = None
        pwda = None
        while pwda == None:
            pwda = input("        请 输 入 金 巴 登 录 密 码：")
        buyers.append({"uname": unam, "pwd": pwda})
    if myChoice == "4":
        clearScreen()
        print("="*20 + "设 置 SMTP 信 息 和 电 邮 接 收 人" + "="*20)
        smtphost = None
        while smtphost == None:
            smtphost = input("        请 输 入 SMTP 服 务 器：")
        smtpport = None
        while smtpport == None:
            smtpport = int(input("        请 输 入 SMTP 端 口："))
        mysendemail = None
        while mysendemail == None:
            mysendemail = input("        请 输 入 SMTP 发 送 电 邮：")
            if not validate_email(mysendemail):
                mysendemail = None
        smtppwd = None
        while smtppwd == None:
            smtppwd = input("        请 输 入 SMTP 密 码：")
        myemailadd = None
        while myemailadd != "quit":
            myemailadd = input("        请 输 入 电 邮 接 收 人（quit 为退出）：")
            if (not validate_email(myemailadd) and myemailadd != "quit"):
                myemailadd = None
            else:
                if myemailadd != None and myemailadd != "quit":
                    emailreceivers.append(myemailadd)
    if myChoice == "5":
        clearScreen()
        print("="*20 + "设 置 出 发 日 期" + "="*20)
        date = None
        while date == None:
            date = input("        请 输 入 出 发 日 期 （格 式 ：YYYY-MM-DD）：")
            if not validate_date(date):
                date = None
    if myChoice == "7":
        info = {
                "uname": uname,
                "pwd": pwd,
                "route": route,
                "date": date,
                "passengers": passengers,
                "mysendemail": mysendemail,
                "emailreceivers": emailreceivers,
                "smtppwd": smtppwd,
                "smtphost": smtphost,
                "smtpport": smtpport,
                "time": time_,
                "track": track,
                "monitors": monitors,
                "autopay": autopay
            }
        info_json = json.dumps(info, indent=2, ensure_ascii=False)
        with open("info.json", "w") as myinfofile:
            myinfofile.write(info_json)
    if myChoice == "8":
        clearScreen()
        print("="*20 + "设 置 出 发 时 间" + "="*20)
        time_ = None
        while time_ == None:
            time_ = input("        请 输 入 出 发 时 间 （格 式 ：HH:MM:SS）：")
            if not validate_time(time_):
                time_ = None
    if myChoice == "9":
        clearScreen()
        print("="*20 + "导 入 轨 迹" + "="*20)
        track = input("        请 输 入 轨 迹 （可 从 guiji.html 获 取）:")
    if myChoice == "10":
        clearScreen()
        print("="*20+"设 置 余 票 账 号 登 录 信 息" + "="*20)
        unam = None
        while unam == None:
            unam = input("        请 输 入 金 巴 登 录 电 邮：")
            if not validate_email(unam):
                unam = None
        pwda = None
        while pwda == None:
            pwda = input("        请 输 入 金 巴 登 录 密 码：")
        monitors.append({"uname": unam, "pwd": pwda})
    if myChoice == "11":
        clearScreen()
        print("="*20+"设 置 支 付 电 邮" + "="*20)
        autopay = None
        while autopay != "Y" and autopay != "N":
            autopay = input("        开 启 支 付 电 邮？(Y: 是，N: 否)：")
        autopay = (autopay == "Y")