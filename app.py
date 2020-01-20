# -*- coding: UTF-8 -*-

import os
import requests
import flask
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from moviehelper import use_moviename_serch_movielist, use_movieurl_get_movieinfo, search_movie_thisweekAndIntheaters

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
    userpostback = event.postback.data
    print(userpostback)

    if userpostback[:71] == 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=':
        movielist, pagebox = use_moviename_serch_movielist(userpostback, '1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    if userpostback[:43] == 'https://movies.yahoo.com.tw/movieinfo_main/':
        moviePosterContant, infoContant, storyContant, actorContant, stillsContant = use_movieurl_get_movieinfo(
            userpostback)
        line_bot_api.reply_message(
            event.reply_token, [moviePosterContant, infoContant, storyContant, actorContant, stillsContant])
    if userpostback[:47] == 'https://movies.yahoo.com.tw/movie_thisweek.html':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_thisweek.html?page=',userpostback[53:])
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    if userpostback[:49] == 'https://movies.yahoo.com.tw/movie_intheaters.html':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_intheaters.html?page=',userpostback[55:])
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])

# ---------------------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userMessage = event.message.text
    
    if userMessage == '製作團隊':
        line_bot_api.reply_message(event.reply_token,)
    elif userMessage == '近期上映':
        
    elif userMessage == '本週新片':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_thisweek.html?page=','1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    elif userMessage == '上映中':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_intheaters.html?page=','1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
        print(movie_intheaters)
    elif userMessage == '排行榜':
        print(userMessage)
    elif userMessage == '類型找電影':
        print(userMessage)
    elif userMessage == '附近影城':
        print(userMessage)
    elif userMessage == '電影時刻':
        print(userMessage)
    else:
        movielist, pagebox = use_moviename_serch_movielist(userMessage, '1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])


# ---------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
