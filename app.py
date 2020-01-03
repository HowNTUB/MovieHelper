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

    print(body)
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
        #中文轉URL格式編碼
        urlname = parse.quote(name)
        #電影清單URL
        movieURL = 'https://movies.yahoo.com.tw/moviesearch_result.html?keyword=' + urlname
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        req = request.Request(movieURL, headers=headers)
        resp = request.urlopen(req)
        respData = str(resp.read().decode('utf-8'))
        soup = BeautifulSoup(respData, "html.parser")
        #抓電影名稱
        rating_selector_name = ".release_movie_name > a"
        rating_name = [i.text for i in soup.select(rating_selector_name)]
        #抓圖片
        rating_selector_img = ".release_foto img"
        rating_img = soup.select(rating_selector_img)
        imglist = []
        for img in rating_img:
            imglist.append(img["src"])
        #抓詳細資料網址
        rating_selector_url = ".release_movie_name > a"
        rating_url = soup.select(rating_selector_url)
        urllist = []
        for url in rating_url:
            urllist.append(url["href"])
        #內容轉為json格式
        contents=[]
        for index in range(len(imglist)):
            contents.append({
                    "type": "bubble",
                    "direction": "ltr",
                    "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "電影(Movie)",
                        "size": "xl",
                        "align": "start",
                        "weight": "bold",
                        "color": "#000000"
                        }
                    ]
                    },
                    "hero": {
                    "type": "image",
                    "url": imglist[index],
                    "gravity": "top",
                    "size": "full",
                    "aspectRatio": "1:1.4",
                    "aspectMode": "cover",
                    "backgroundColor": "#FFFFFF"
                    },
                    "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "text",
                            "text": rating_name[index],
                            "margin": "none",
                            "size": "lg",
                            "align": "center",
                            "gravity": "top",
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": "YAOAN"
                            }
                        ]
                        },
                        {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#FFFFFF"
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": "上映日期："
                            },
                            {
                            "type": "text",
                            "text": "1999-10-22"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": "期待度：",
                            "align": "start",
                            "weight": "bold",
                            "color": "#BB21CA"
                            },
                            {
                            "type": "text",
                            "text": "87%"
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                            "type": "text",
                            "text": "滿意度：",
                            "align": "start",
                            "weight": "bold",
                            "color": "#2133CA"
                            },
                            {
                            "type": "text",
                            "text": "3.7",
                            "align": "start"
                            }
                        ]
                        }
                    ]
                    },
                    "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "詳細資料",
                            "text": "詳細資料",
                            "data": "postbackcontect"
                        },
                        "color": "#B0B0B0"
                        }
                    ]
                    }
                ,
                    "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "詳細資料",
                            "text": "詳細資料",
                            "data": urllist[index]
                        },
                        "color": "#B0B0B0"
                        }
                    ]
                    }
                    })
        #彈性訊息
        flex_message = FlexSendMessage(
            alt_text='movielist',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )
        #回復
        line_bot_api.reply_message(event.reply_token, flex_message)
    except Exception as e:
        print(str(e))


# ---------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
