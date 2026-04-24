# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# import time
# import os


# def main():
#     options = Options()
#     # 1. 开启隐身模式
#     options.add_argument("--incognito")

#     # 2. 移除 "Chrome 正在受到自动测试软件的控制" 的提示条
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("useAutomationExtension", False)
#     options.add_argument("--headless")  # 无头模式（推荐在 CI 中使用）
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     options.add_argument("--disable-gpu")
#     options.add_argument("--window-size=1920,1080")
#     os.makedirs("screenshots", exist_ok=True)
#     # Selenium 4.6+ 使用 Selenium Manager，自动处理 ChromeDriver
#     driver = webdriver.Chrome(options=options)

#     # 3. 通过 CDP (Chrome DevTools Protocol) 在页面加载前执行 JS，抹除 webdriver 痕迹
#     driver.execute_cdp_cmd(
#         "Page.addScriptToEvaluateOnNewDocument",
#         {
#             "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#         get: () => undefined
#         })
#     """
#         },
#     )

#     driver.get("https://ikuuu.org/user")
#     time.sleep(2)
#     wait = WebDriverWait(driver, 15)
#     # ====================== 1. 点击极验验证按钮 ======================
#     try:
#         driver.save_screenshot("screenshots/01_after_click_geetest1.png")
#         geetest_btn = wait.until(
#             EC.element_to_be_clickable(
#                 (By.CSS_SELECTOR, "div[class*='geetest_btn_click']")
#             )
#         )
#         print("找到极验按钮，正在点击...")
#         geetest_btn.click()
#         time.sleep(2.5)  # 等待验证码加载

#         driver.save_screenshot("screenshots/01_after_click_geetest.png")

#     except Exception as e:
#         print("点击极验按钮失败:", e)
#         driver.save_screenshot("screenshots/geetest_click_fail.png")

#     # ====================== 2. 填写邮箱 ======================
#     try:
#         driver.save_screenshot("screenshots/02_after_fill_email2.png")

#         email_input = wait.until(EC.element_to_be_clickable((By.ID, "email")))
#         email_input.clear()
#         email_input.send_keys("你的邮箱@example.com")  # ← 修改成你的邮箱
#         print("✅ 邮箱填写完成")
#         driver.save_screenshot("screenshots/02_after_fill_email.png")
#     except Exception as e:
#         print("填写邮箱失败:", e)
#         driver.save_screenshot("screenshots/email_fail.png")

#     # ====================== 3. 填写密码 ======================
#     try:
#         driver.save_screenshot("screenshots/03_after_fill_password3.png")

#         password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
#         password_input.clear()
#         password_input.send_keys("你的真实密码")  # ← 修改成你的密码
#         print("✅ 密码填写完成")
#         driver.save_screenshot("screenshots/03_after_fill_password.png")
#     except Exception as e:
#         print("填写密码失败:", e)
#         driver.save_screenshot("screenshots/password_fail.png")
#     finally:
#         driver.quit()


# if __name__ == "__main__":
#     main()


import json
import time
import os
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_main_version():
    # 获取驱动管理器检测到的安装版本（例如 "123.0.6312.122"）
    full_version = ChromeDriverManager().driver.get_browser_version_from_os()
    # 提取主版本号 (例如 "123")
    main_version = int(full_version.split(".")[0])
    return main_version


def save_cookies():
    options = uc.ChromeOptions()
    # 模拟真实浏览器特征
    options.add_argument("--window-size=1920,1080")
    os.makedirs("screenshots", exist_ok=True)

    # 使用 context manager (with 语句) 可以自动处理资源回收，减少句柄报错
    try:
        # driver = uc.Chrome(options=options, version_main=147)
        options.add_argument("--headless")  # 必须：无界面模式
        options.add_argument("--no-sandbox")  # 必须：解决权限问题
        options.add_argument("--disable-dev-shm-usage")  # 必须：防止内存不足
        options.add_argument("--remote-debugging-port=9222")  # 建议：有助于连接稳定
        # driver = uc.Chrome(options=options)
        version = get_chrome_main_version()
        print(f"🚀 检测到 Chrome 主版本: {version}")
        driver = uc.Chrome(options=options, version_main=version)
        # driver.get("https://ikuuu.org/auth/login")

        # print("🚀 浏览器已启动。")
        # print("💡 请在 60 秒内完成：1.输入账号密码 2.通过极验验证 3.点击登录")

        # # 优化：循环检测是否登录成功，不需要死等 60 秒
        # for i in range(60):
        #     if "user" in driver.current_url:
        #         print("\n检测到已进入后台，登录成功！")
        #         break
        #     if i % 5 == 0:
        #         print(f"等待中... 剩余 {60-i}s", end="\r")
        #     time.sleep(1)

        # # 获取当前域名的 cookies
        # cookies = driver.get_cookies()
        # with open("ikuuu_cookies.json", "w") as f:
        #     json.dump(cookies, f)

        # print("\n✅ Cookies 已保存到 ikuuu_cookies.json")
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
            email_input.send_keys("chen540605375@gmail.com")  # ← 修改成你的邮箱
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
            password_input.send_keys("wodemima4DAxie@")  # ← 修改成你的密码
            print("✅ 密码填写完成")
            driver.save_screenshot("screenshots/03_after_fill_password.png")
        except Exception as e:
            print("填写密码失败:", e)
            driver.save_screenshot("screenshots/password_fail.png")

        try:
            # 定位包含 .login 类的 submit 按钮
            login_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.login"))
            )
            print("找到登录按钮，正在点击...")
            login_btn.click()
            print("✅ 登录按钮已点击")
            driver.save_screenshot("screenshots/04_after_fill_login.png")

        except Exception as e:
            print("点击登录按钮失败:", e)

        # 优化：循环检测是否登录成功，不需要死等 60 秒
        for i in range(60):
            if "user" in driver.current_url:
                print("\n检测到已进入后台，登录成功！")
                break
            if i % 5 == 0:
                print(f"等待中... 剩余 {60-i}s", end="\r")
            time.sleep(1)
        driver.save_screenshot("screenshots/04_login.png")

        # 获取当前域名的 cookies
        cookies = driver.get_cookies()
        with open("screenshots/ikuuu_cookies.json", "w") as f:
            json.dump(cookies, f)
        # finally:
        #     driver.quit()
        # --- 关键修改 2: 保持 Python 进程存活，防止浏览器因为父进程死亡而关闭 ---

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
    finally:
        # 显式退出，并捕获 Windows 句柄异常
        # try:
        #     driver.quit()
        # except:
        pass


def login_with_cookies():
    options = uc.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # 1. 必须先访问一次域名，建立 context
    driver.get("https://ikuuu.org")

    # 2. 读取保存的 cookies
    with open("screenshots/ikuuu_cookies.json", "r") as f:
        cookies = json.load(f)

    # 3. 注入 Cookies
    for cookie in cookies:
        # 如果 cookie 包含 expiry 字段，部分浏览器可能会报错，可以尝试删除它
        if "expiry" in cookie:
            del cookie["expiry"]
        driver.add_cookie(cookie)

    # 4. 刷新页面，此时应该是登录状态
    driver.refresh()
    driver.get("https://ikuuu.org/user")  # 直接跳转后台


if __name__ == "__main__":
    # 必须在 Windows 下使用此判断，防止多进程递归启动
    save_cookies()
    # while True:
    #     time.sleep(100)
