from flask import Flask, request
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import os
from selenium import webdriver
from urllib import parse
stealthminjs = None
with open('stealth.min.js', 'r') as f:
    stealthminjs = f.read()
app = Flask(__name__)

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

@app.route('/captcha', methods=['POST'])
def captcha():
    global GUIJIHTML
    s1 = time.time()
    appid = request.json["appId"]
    scene = request.json["scene"]
    MYHTMLFILE = GUIJIHTML.replace("MYAPPID", appid).replace("MYSCENE", scene)
    with open("guiji.html", "w", encoding="UTF-8") as myh:
        myh.write(MYHTMLFILE)
    s2 = time.time()
    print("Stage 1 done.")
    browser = None
    try:
        from selenium.webdriver.firefox.options import Options
        from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
        options = Options()
        options.headless = True
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0")
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX
        browser = webdriver.Firefox(options=options,firefox_profile=profile, desired_capabilities=desired)
    except Exception:
        myRandomChromeUA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        print("Your useragent is", myRandomChromeUA, ".")
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("user-agent="+myRandomChromeUA)
        options.add_argument("--headless")
        browser = webdriver.Chrome(options=options)
        # 调用函数在页面加载前执行脚本
        browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': stealthminjs})
    browser.get(os.path.abspath("guiji.html"))
    slideBtn = browser.find_element_by_css_selector(".btn_slide")
    slideOffsetWidth = browser.execute_script("return (document.querySelector(\".nc_scale\").clientWidth - document.querySelector(\".nc_iconfont\").clientWidth);")
    actions = ActionChains(browser)
    offsets = [] # 规避可疑轨迹
    while slideOffsetWidth > 0:
        myOffset = random.randint(50, 120)
        if slideOffsetWidth < myOffset:
            myOffset = slideOffsetWidth
        slideOffsetWidth -= myOffset
        offsets.append(myOffset)
    print("Track:", offsets)
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
    s3 = time.time()
    print(f"Stage 2 done.\nStage 1 took {s2-s1} seconds.")
    print(f"Stage 2 took {s3-s2} seconds.")
    return myData


app.run(host="0.0.0.0", port=8001)
