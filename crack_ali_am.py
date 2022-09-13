import requests
import json
import time
import random
import requests
from selenium.webdriver.common.action_chains import ActionChains
import os
from pyvirtualdisplay import Display
from selenium import webdriver
from urllib import parse
stealthminjs = None
with open('stealth.min.js', 'r') as f:
    stealthminjs = f.read()

GUIJIHTML = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <script src="https://g.alicdn.com/AWSC/AWSC/awsc.js"></script>
</head>
<body>
<div id="nc"></div>
<script>
    // 实例化nc
    AWSC.use("nc", function (state, module) {
        // 初始化
        window.nc = module.init({
            // 应用类型标识。它和使用场景标识（scene字段）一起决定了滑动验证的业务场景与后端对应使用的策略模型。您可以在阿里云验证码控制台的配置管理页签找到对应的appkey字段值，请务必正确填写。
            appkey: "MYAPPID",
            //使用场景标识。它和应用类型标识（appkey字段）一起决定了滑动验证的业务场景与后端对应使用的策略模型。您可以在阿里云验证码控制台的配置管理页签找到对应的scene值，请务必正确填写。
            scene: "MYSCENE",
            // 声明滑动验证需要渲染的目标ID。
            renderTo: "nc",
            //前端滑动验证通过时会触发该回调参数。您可以在该回调参数中将会话ID（sessionId）、签名串（sig）、请求唯一标识（token）字段记录下来，随业务请求一同发送至您的服务端调用验签。
            success: function (data) {
                document.body.innerHTML += "<br /><br /><h2>打码成功！</h2><p><textarea id=\\"mync\\">" + JSON.stringify(data) + "</textarea></p>";
            },
            // 滑动验证失败时触发该回调参数。
            fail: function (failCode) {
                document.body.innerHTML += "<br /><br /><h2>打码失败！</h2><p><textarea id=\\"mync\\">" + JSON.stringify(failCode) + "</textarea></p>";
            },
            // 验证码加载出现异常时触发该回调参数。
            error: function (errorCode) {
                document.body.innerHTML += "<br /><br /><h2>验证码出现异常！</h2><p><textarea id=\\"mync\\">" + JSON.stringify(errorCode) + "</textarea></p>";
            }
        });
    })
</script>
</body>
</html>'''
def slide(session, headers, referrerURL, APPID, scene, ncSessionID, TRACK):
    global GUIJIHTML
    myid = "".join(str(random.random()).split("."))
    s1 = time.time()
    MYHTMLFILE = GUIJIHTML.replace("MYAPPID", APPID).replace("MYSCENE", scene)
    with open(f"guiji{myid}.html", "w", encoding="UTF-8") as myh:
        myh.write(MYHTMLFILE)
    s2 = time.time()
    try:
        if os.name == "posix":
            display = Display(visible=0, size=(1024, 768))
            display.start()
        myRandomChromeUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        print("Your useragent is", myRandomChromeUA, ".")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent="+myRandomChromeUA)
        options.add_argument("--headless")
        if os.name == "posix":
            options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(options=options)
        # 调用函数在页面加载前执行脚本
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': stealthminjs})
    except Exception as e:
        print("失败")
        return None
    print("Stage 1 done.")
    browser.get("file://"+os.path.abspath(f"guiji{myid}.html"))
    slideBtn = None
    while True:
        try:
            slideBtn = browser.find_element_by_css_selector(".btn_slide")
        except Exception:
            pass
        break
    slideOffsetWidth = browser.execute_script("return (document.querySelector(\".nc_scale\").clientWidth - document.querySelector(\".nc_iconfont\").clientWidth);")
    actions = ActionChains(browser, duration=0)
    offsets = [] # 规避可疑轨迹
    while slideOffsetWidth > 0:
        myOffset = random.randint(140, 160)
        if slideOffsetWidth < myOffset:
            myOffset = slideOffsetWidth
        slideOffsetWidth -= myOffset
        offsets.append(myOffset)
    print("Track:", offsets)
    actions.w3c_actions.pointer_action._duration = 0
    actions.click_and_hold(slideBtn).perform()
    for slideWidth in offsets:
        actions.move_by_offset(xoffset=slideWidth,yoffset=0).perform()
    actions.release().perform()
    print("Captcha done.")
    myData = None
    while myData == None:
        try:
            myData = browser.find_element_by_css_selector("#mync").get_attribute("innerHTML")
        except Exception:
            myData = None
    occupied = False
    s3 = time.time()
    print(f"Stage 2 done.\nStage 1 took {s2-s1} seconds.")
    print(f"Stage 2 took {s3-s2} seconds.")
    myData = json.loads(myData)
    if type(myData).__name__ != "dict":
        print("破解失败。")
        return None
    else:
        print(myData)
        print("破解成功。")
    return myData
"""    try:
        mySlider = requests.post("http://localhost:8001/captcha", json={
            "appId": APPID,
            "scene": scene
        }).json()
        print(mySlider)
        print("验证码破解成功")
        return mySlider
    except Exception:
        print("验证码破解失败")
        return None
"""
