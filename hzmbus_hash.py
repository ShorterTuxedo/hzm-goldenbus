from selenium import webdriver
import os
import json
class HZMHash():
    def __init__(self, activate=False, url="https://i.hzmbus.com/webhtml/index.html"):
        self.activated = activate
        self.browser = None
        if activate:
            self.activate_browser(url)
    def activate_browser(self, url="https://i.hzmbus.com/webhtml/index.html"):
        stealthminjs = None
        with open('stealth.min.js', 'r') as f:
            stealthminjs = f.read()
        if self.browser != None:
            self.browser.quit()
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
            self.browser = webdriver.Chrome(options=options)
            # 调用函数在页面加载前执行脚本
            self.browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {'source': stealthminjs})
        except Exception as e:
            print("失败")
        self.browser.get(url)
        self.activated = True
    def msk6(self, data):
        if self.activated and self.browser != None:
            return self.browser.execute_script("return msk6(" + json.dumps(data, ensure_ascii=False) + ");")
    def cs(self, data):
        if self.activated and self.browser != None:
            return self.browser.execute_script("return cs(" + json.dumps(data, ensure_ascii=False) + ");")
    def ft(self, data):
        if self.activated and self.browser != None:
            return self.browser.execute_script("return ft(" + json.dumps(data, ensure_ascii=False) + ");")
    def set_token_web(self, data):
        if self.activated and self.browser != None:
            return self.browser.execute_script("return setTokenWeb('" + json.dumps(data, ensure_ascii=False) + "');")
        return data
