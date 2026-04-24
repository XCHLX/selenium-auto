from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os


def save_cookies():

    options = Options()

    # 1. 开启隐身模式
    options.add_argument("--incognito")
    os.makedirs("screenshots", exist_ok=True)
    # 2. 移除 "Chrome 正在受到自动测试软件的控制" 的提示条
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    # 3. 通过 CDP (Chrome DevTools Protocol) 在页面加载前执行 JS，抹除 webdriver 痕迹
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
        },
    )
    driver.get("https://ikuuu.org/user")
    time.sleep(2)
    wait = WebDriverWait(driver, 15)
    # ====================== 1. 点击极验验证按钮 ======================
    try:
        driver.save_screenshot("screenshots/01_after_click_geetest1.png")
        geetest_btn = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div[class*='geetest_btn_click']")
            )
        )
        print("找到极验按钮，正在点击...")
        geetest_btn.click()
        time.sleep(2.5)  # 等待验证码加载

        driver.save_screenshot("screenshots/01_after_click_geetest.png")

    except Exception as e:
        print("点击极验按钮失败:", e)
        driver.save_screenshot("screenshots/geetest_click_fail.png")

    # ====================== 2. 填写邮箱 ======================
    try:
        driver.save_screenshot("screenshots/02_after_fill_email2.png")

        email_input = wait.until(EC.element_to_be_clickable((By.ID, "email")))
        email_input.clear()
        email_input.send_keys("你的邮箱@example.com")  # ← 修改成你的邮箱
        print("✅ 邮箱填写完成")
        driver.save_screenshot("screenshots/02_after_fill_email.png")
    except Exception as e:
        print("填写邮箱失败:", e)
        driver.save_screenshot("screenshots/email_fail.png")

    # ====================== 3. 填写密码 ======================
    try:
        driver.save_screenshot("screenshots/03_after_fill_password3.png")

        password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_input.clear()
        password_input.send_keys("你的真实密码")  # ← 修改成你的密码
        print("✅ 密码填写完成")
        driver.save_screenshot("screenshots/03_after_fill_password.png")
    except Exception as e:
        print("填写密码失败:", e)
        driver.save_screenshot("screenshots/password_fail.png")
    finally:
        driver.quit()


if __name__ == "__main__":
    # 必须在 Windows 下使用此判断，防止多进程递归启动
    save_cookies()
