# -*- coding: UTF-8 -*-

import requests
import os
import flask
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


app = flask.Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    '4O8vNwJN4S3g6m6UtTe6T9hhUW0rXnIH4aK52CMEJFL53XyzQQkZZg5o90w8y1p9+Zlh5D+v3LVaymuIt1Mh8PSd7+2RYM+2NxJyQguGY7qE/GI0Ttwbzk5HmMmBS2RSzjzSIzVPgE7WyNQCDLPpywdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('318d67366cb286f75b9894da10dc36af')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = flask.request.headers['X-Line-Signature']
    # get request body as text
    body = flask.request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        flask.abort(400)
    return 'OK'

# ---------------------------------------------------------------
# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        name = event.message.text
        urlname = parse.quote(name)
        movieURL = 'https://movies.yahoo.com.tw/moviesearch_result.html?keyword=' + urlname
        print(movieURL)
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        req = request.Request(movieURL, headers=headers)
        resp = request.urlopen(req)
        respData = str(resp.read().decode('utf-8'))
        soup = BeautifulSoup(respData, "html.parser")

        rating_selector_name = ".release_movie_name > a"
        rating_name = [i.text for i in soup.select(rating_selector_name)]

        rating_selector_img = ".release_foto img"
        rating_img = soup.select(rating_selector_img)
        imglist = []
        for img in rating_img:
            imglist.append(img["src"])

        rating_selector_url = ".release_movie_name > a"
        rating_url = soup.select(rating_selector_url)
        urllist = []
        for url in rating_url:
            urllist.append(url["href"])

        flex_message = FlexSendMessage(
            alt_text='hello',
            contents={
                'type': 'bubble',
                'direction': 'ltr',
                'hero': {
                    'type': 'image',
                    'url': 'https://example.com/cafe.jpg',
                    'size': 'full',
                    'aspectRatio': '20:13',
                    'aspectMode': 'cover',
                    'action': { 'type': 'uri', 'uri': 'http://example.com', 'label': 'label' }
                }
            }
        )

        line_bot_api.reply_message(event.reply_token, flex_message)
    except Exception as e:
        print(str(e))


# ---------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
