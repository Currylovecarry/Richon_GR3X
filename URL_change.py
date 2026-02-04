import requests
import time
import hashlib
from datetime import datetime
import os

# 监控配置
URL = "https://newsite.ricn-mall.com/goods_cate?cid=9"
CHECK_INTERVAL = 20


def get_page_hash():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status()
        # 使用哈希值快速对比内容是否变化
        return hashlib.sha224(response.text.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"[{datetime.now()}] 错误: {e}")
        return None


def monitor():
    print(f"开始监控: {URL}")
    last_hash = get_page_hash()

    while True:
        time.sleep(CHECK_INTERVAL)
        current_hash = get_page_hash()

        if current_hash and current_hash != last_hash:
            print(f"[{datetime.now()}] 警告：检测到页面已更改！")
            # 在这里调用通知函数（如发邮件、发钉钉/企业微信机器人等）
            send_notification("页面发生变化了！")
            last_hash = current_hash
        else:
            print(f"[{datetime.now()}] 页面未变化...")


def send_notification(msg):
    print(f"发送通知: {msg}")

    # 播放提示音（跨平台兜底方案）
    try:
        # macOS
        os.system('afplay /System/Library/Sounds/Ping.aiff')
    except:
        try:
            # Windows
            os.system('echo \a')
        except:
            pass


if __name__ == "__main__":
    monitor()