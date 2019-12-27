# -*- coding: UTF-8 -*-

from bs4 import BeautifulSoup
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    '4O8vNwJN4S3g6m6UtTe6T9hhUW0rXnIH4aK52CMEJFL53XyzQQkZZg5o90w8y1p9+Zlh5D+v3LVaymuIt1Mh8PSd7+2RYM+2NxJyQguGY7qE/GI0Ttwbzk5HmMmBS2RSzjzSIzVPgE7WyNQCDLPpywdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('318d67366cb286f75b9894da10dc36af')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# ---------------------------------------------------------------
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if(event.message.text == "movie"):
        from urllib import request
        from bs4 import BeautifulSoup
        try:
            url = 'https://movies.yahoo.com.tw/'
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
            soup = BeautifulSoup(respData)

            rating_selector_name = ".text_truncate_1"
            rating_name = [i.text for i in soup.select(rating_selector_name)][0]
            line_bot_api.reply_message(event.reply_token, rating_name)
        except Exception as e:
            print(str(e))
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)

# ---------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
