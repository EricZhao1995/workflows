from urllib import request, parse
import requests

import pandas as pd
import json

url="https://api.seniverse.com/v3/weather/daily.json?key=ST3HlYrJOeRT64FAX&location=shanghai&language=zh-Hans&unit=c&start=0&days=5"

# 构建请求
req = request.Request(url)
# 发送请求，读取返回值并进行 UTF-8 编码
response = request.urlopen(req).read().decode('UTF-8')
response = json.loads(response)

# 提取 daily 数据
df = pd.DataFrame(response["results"][0]["daily"])

# 选择需要的列，并修改列名
df = df[["date", "text_day", "high", "low", "rainfall", "humidity", "wind_scale"]]
df.columns = ["日期", "天气", "最高温(°C)", "最低温(°C)", "降水量(mm)", "湿度(%)", "风力"]

# 设置索引为日期
df.set_index("日期", inplace=True)

url2 = "https://open.f.mioffice.cn/open-apis/bot/v2/hook/74c5bdbc-1276-4c49-a6e8-c1f455752379"

daily_forecast = response["results"][0]["daily"]
message = "上海未来三天天气预报：\n"
for day in daily_forecast:
    message += f"{day['date']}: {day['text_day']}，气温{day['low']}~{day['high']}°C，降水量{day['rainfall']}mm，湿度{day['humidity']}%，风力{day['wind_scale']}级\n"

# 构造 POST 请求的 payload
payload = {
    "msg_type": "text",  # 适用于飞书、钉钉等
    "content": {"text": message}
}

# 发送 POST 请求
headers = {"Content-Type": "application/json"}
response = requests.post(url2, data=json.dumps(payload), headers=headers)

# 打印响应
print(response.status_code, response.text)