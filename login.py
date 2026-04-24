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


def save_cookies():
    options = uc.ChromeOptions()
    # 模拟真实浏览器特征
    options.add_argument("--window-size=1920,1080")
    os.makedirs("screenshots", exist_ok=True)

    # 使用 context manager (with 语句) 可以自动处理资源回收，减少句柄报错
    try:
        driver = uc.Chrome(options=options, version_main=147)
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

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
    finally:
        # 显式退出，并捕获 Windows 句柄异常
        try:
            driver.quit()
        except:
            pass


if __name__ == "__main__":
    # 必须在 Windows 下使用此判断，防止多进程递归启动
    save_cookies()
