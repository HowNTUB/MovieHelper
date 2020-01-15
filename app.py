# -*- coding: UTF-8 -*-

import requests
import flask
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from moviehelper import use_moviename_serch_movielist, use_movieurl_get_movieinfo

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
    infoContant, actorContant, introductionContant = use_movieurl_get_movieinfo(event.postback.data)
    line_bot_api.reply_message(event.reply_token,[infoContant, actorContant, introductionContant])

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