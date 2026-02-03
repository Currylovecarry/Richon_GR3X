import requests
import time

# ================= 配置区 =================
# 1. Pushdeer 的 Key（在这里填入你的 Key）
PUSHDEER_KEY = "你的Pushdeer_Key"

# 2. 监控关键词
KEYWORDS = ["官翻品"]

# 3. 检查频率（秒），抢官翻建议设为 30-60 秒
CHECK_INTERVAL = 60

# 4. 接口配置
URL = "https://newsite.ricn-mall.com/api/pc/get_products"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJuZXdzaXRlLnJpY24tbWFsbC5jb20iLCJhdWQiOiJuZXdzaXRlLnJpY24tbWFsbC5jb20iLCJpYXQiOjE3NzAwMzQ2NjIsIm5iZiI6MTc3MDAzNDY2MiwiZXhwIjoxNzcyNjI2NjYyLCJqdGkiOnsiaWQiOjUzMTM1LCJ0eXBlIjoiYXBpIn19.c_4w3VuRAPdWo11CFaeZcq9VcHHuVa2qgSB9nlBoL80",
    "Cookie": "auth._token.local1=Bearer%20eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...; auth.strategy=local1; PHPSESSID=e99f905a3cd87aedbe73bd581a351376; cb_lang=zh-cn",
    "Form-type": "pc"
}


# ==========================================

def send_wechat_msg(content):
    """发送微信提醒"""
    push_url = "https://api2.pushdeer.com/message/push"
    payload = {
        "pushkey": PUSHDEER_KEY,
        "text": "🔥 理光相机有货通知！",
        "desp": content,
        "type": "markdown"
    }
    try:
        requests.post(push_url, data=payload)
    except Exception as e:
        print(f"微信发送失败: {e}")


def check_stock():
    params = {"page": 1, "limit": 20, "cid": 9, "sid": 0}
    try:
        # 强制处理 latin-1 编码隐患
        response = requests.get(URL, params=params, headers=HEADERS, timeout=15)

        if response.status_code == 200:
            data = response.json()
            products = data.get('data', {}).get('list', [])

            for item in products:
                name = item.get('store_name', '')
                stock = item.get('stock', 0)
                price = item.get('price', '未知')

                # 匹配关键词
                if all(k.upper() in name.upper() for k in KEYWORDS):
                    if stock > 0:
                        msg = f"检测到：{name}\n\n库存：{stock}\n价格：{price}\n\n[点击前往官网](https://newsite.ricn-mall.com/)"
                        print(f"【发现现货】{name}")
                        send_wechat_msg(msg)
                        return True  # 发现有货后可选择是否停止
                    else:
                        print(f"{time.strftime('%H:%M:%S')} - 监控中: {name} (目前缺货)")
        elif response.status_code == 401:
            print("❌ Token 已失效，请重新登录获取！")
            send_wechat_msg("⚠️ 监控脚本 Token 失效，请更新！")
    except Exception as e:
        print(f"监控请求出错: {e}")
    return False


if __name__ == "__main__":
    print(f"理光库存微信监控已启动... 关键词: {KEYWORDS}")
    while True:
        check_stock()
        time.sleep(CHECK_INTERVAL)