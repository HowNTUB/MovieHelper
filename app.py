# -*- coding: UTF-8 -*-

import os
import requests
import flask
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from moviehelpermodule.moviehelper import use_moviename_serch_movielist, use_moviename_serch_article, use_movieurl_get_movieinfo, search_movie_thisweekAndIntheaters, search_movie_comingsoon, search_movie_chart, select_movie_type, search_movie_type, use_location_search_movietheater, workTeam

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
    
    #電影清單
    if userpostback[:71] == 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=':
        movielist, pagebox = use_moviename_serch_movielist(userpostback, '')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    #電影詳細資料
    if userpostback[:43] == 'https://movies.yahoo.com.tw/movieinfo_main/':
        moviePosterContant, infoContant, storyContant, actorContant, stillsContant = use_movieurl_get_movieinfo(
            userpostback)
        line_bot_api.reply_message(
            event.reply_token, [moviePosterContant, infoContant, storyContant, actorContant, stillsContant])
    #即將上映
    if userpostback[:49] == 'https://movies.yahoo.com.tw/movie_comingsoon.html':
        movietab, movielist, pagebox = search_movie_comingsoon(userpostback)
        line_bot_api.reply_message(event.reply_token, [movietab, movielist, pagebox])
    #本週新片 上映中
    if userpostback[:47] == 'https://movies.yahoo.com.tw/movie_thisweek.html' or userpostback[:49] == 'https://movies.yahoo.com.tw/movie_intheaters.html':
        movielist, pagebox = search_movie_thisweekAndIntheaters(userpostback)
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    #類型找電影
    movieType = ['動作','冒險','科幻','奇幻','劇情','犯罪','恐怖','懸疑驚悚','喜劇','愛情','溫馨家庭','動畫','戰爭','音樂歌舞','歷史傳記','紀錄片','勵志','武俠','影展','戲劇','影集']
    if userpostback in movieType:
        line_bot_api.reply_message(event.reply_token, search_movie_type(userpostback, ''))
    if userpostback[:60] == 'https://movies.yahoo.com.tw/moviegenre_result.html?genre_id=':
        line_bot_api.reply_message(event.reply_token, search_movie_type('', userpostback))
    
# ---------------------------------------------------------------
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userMessage = event.message.text
    print(event)
    if userMessage == '製作團隊':
        line_bot_api.reply_message(event.reply_token,workTeam())
    elif userMessage == '即將上映':
        movietab, movielist, pagebox = search_movie_comingsoon('')
        line_bot_api.reply_message(event.reply_token, [movietab, movielist, pagebox])
    elif userMessage == '本週新片':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_thisweek.html?page=1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
    elif userMessage == '上映中':
        movielist, pagebox = search_movie_thisweekAndIntheaters('https://movies.yahoo.com.tw/movie_intheaters.html?page=1')
        line_bot_api.reply_message(event.reply_token, [movielist, pagebox])
        print()
    elif userMessage == '排行榜':
        movierank = search_movie_chart('https://movies.yahoo.com.tw/chart.html')
        line_bot_api.reply_message(event.reply_token, movierank)
    elif userMessage == '類型找電影':
        line_bot_api.reply_message(event.reply_token, select_movie_type())
    elif userMessage == '附近影城':
        print(userMessage)
    elif userMessage == '電影時刻':
        print(userMessage)
    elif userMessage[:2] == '新聞':
        line_bot_api.reply_message(event.reply_token, use_moviename_serch_article(userMessage[2:]))
    else:
        movielist, pagebox = use_moviename_serch_movielist(userMessage, '1')
        if not pagebox:
            line_bot_api.reply_message(event.reply_token, movielist)
        else:
            line_bot_api.reply_message(event.reply_token, [movielist, pagebox])

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    print(event.message.address)
    print(event.message.latitude)
    print(event.message.longitude)
    radar = use_location_search_movietheater(event.message.address,event.message.latitude,event.message.longitude)
    line_bot_api.reply_message(event.reply_token, radar)

# ---------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)