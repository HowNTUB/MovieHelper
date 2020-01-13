# -*- coding: UTF-8 -*-

import requests
import flask
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from moviehelper import use_moviename_serch_movielist

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
@handler.add(PostbackEvent)
def handle_postback(event):
    print(event.postback.data)
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "電影資訊(Infomation)",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "	 STAR WARS : 天行者的崛起",
                "weight": "bold"
                },
                {
                "type": "text",
                "text": "Star Wars: The Rise of Skywalker",
                "size": "xs"
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": "動作　",
                    "flex": 0,
                    "weight": "bold",
                    "color": "#000C3B"
                    },
                    {
                    "type": "text",
                    "text": "動作　",
                    "flex": 0,
                    "weight": "bold",
                    "color": "#000C3B"
                    },
                    {
                    "type": "text",
                    "text": "動作　",
                    "flex": 0,
                    "weight": "bold",
                    "color": "#000C3B"
                    },
                    {
                    "type": "text",
                    "text": "動作　",
                    "flex": 0,
                    "weight": "bold",
                    "color": "#000C3B"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "sm",
                "contents": [
                    {
                    "type": "text",
                    "text": "上映日期",
                    "weight": "bold"
                    },
                    {
                    "type": "text",
                    "text": "2019-12-18"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xs",
                "contents": [
                    {
                    "type": "text",
                    "text": "片　　長",
                    "weight": "bold"
                    },
                    {
                    "type": "text",
                    "text": "02時22分"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xs",
                "contents": [
                    {
                    "type": "text",
                    "text": "發行公司",
                    "weight": "bold"
                    },
                    {
                    "type": "text",
                    "text": "迪士尼"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "vertical",
                "margin": "xs",
                "contents": [
                    {
                    "type": "text",
                    "text": "導演",
                    "weight": "bold"
                    },
                    {
                    "type": "text",
                    "text": "J.J.亞伯拉罕(J.J. Abrams)"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "vertical",
                "margin": "xs",
                "contents": [
                    {
                    "type": "text",
                    "text": "演員",
                    "weight": "bold"
                    },
                    {
                    "type": "text",
                    "text": "亞當崔佛(Adam Driver) 、 黛西蕾德莉(Daisy Ridley) 、 多姆納爾格里森(Domhnall Gleeson) 、 凱莉羅素(Keri Russell) 、 奧斯卡伊薩克(Oscar Isaac) 、 露琵塔尼詠歐(Lupita Nyong'o) 、 伊恩麥卡達米(Ian McDiarmid ) 、 李察葛蘭(Richard E. Grant)",
                    "size": "xs",
                    "wrap": true
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xs",
                "contents": [
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": "期待度",
                        "weight": "bold",
                        "color": "#BB21CA"
                        },
                        {
                        "type": "text",
                        "text": "90%"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": "滿意度",
                        "weight": "bold",
                        "color": "#2133CA"
                        },
                        {
                        "type": "text",
                        "text": "3.6"
                        }
                    ]
                    }
                ]
                }
            ]
            }
        }
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text=='近期上映':
        text_message = TextSendMessage(text='近期上映的電影清單')
        line_bot_api.reply_message(
            event.reply_token, [
            TextSendMessage(text='Hello World!'),
            TextSendMessage(text='Hello World!')
            ]
        )
    else:
        line_bot_api.reply_message(event.reply_token,use_moviename_serch_movielist(event.message.text))


# ---------------------------------------------------------------
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)