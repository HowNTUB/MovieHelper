from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from linebot.models import *


def use_moviename_serch_movielist(movieName):
    # 中文轉URL格式編碼
    urlname = parse.quote(movieName)
    # 電影清單URL
    movieURL = 'https://movies.yahoo.com.tw/moviesearch_result.html?keyword=' + \
        urlname + '&type=movie'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))
    soup = BeautifulSoup(respData, "html.parser")
    # movieNameCN 中文名
    # movieNameEN 英文名
    # movieExpectation 期待值
    # movieSatisfactoryDegree 滿意度
    # moviePoster 海報
    # movieReleaseTime 上映時間
    # movieDetailUrl 詳細資訊網址

    if soup.select_one(".release_movie_name > a") == None:
        flex_message = FlexSendMessage(
            alt_text='movielist',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "無找到 "+movieName+" 的相關資料",
                            "align": "center"
                        }
                    ]
                }
            }
        )
    else:
        movieInfo = [i.text for i in soup.select(".release_info")]
        movieNameCN = [i.text for i in soup.select(".release_movie_name > a")]
        movieNameEN = [i.text for i in soup.select(".en a")]
        movieExpectation = [i.text for i in soup.select("#content_l dt span")]
        movieSatisfactoryDegree = []
        for info in movieInfo:
            movieSatisfactoryDegree.append('未上映') if info.find(
                "滿意度") == -1 else movieSatisfactoryDegree.append(info[info.find("滿意度")+5:info.find("滿意度")+8])
        movieImg = [i for i in soup.select(".release_foto img")]
        moviePoster = []
        for img in movieImg:
            moviePoster.append(img["src"])
        movieReleaseTimeStr = [i.text for i in soup.select(".time")]
        movieReleaseTime = []
        for date in movieReleaseTimeStr:
            movieReleaseTime.append(date[7:])
        movieDetail = [i for i in soup.select(".release_movie_name > a")]
        movieDetailUrl = []
        for url in movieDetail:
            movieDetailUrl.append(url["href"])

        # 內容轉為json格式
        contents = []
        for index in range(len(movieNameCN)):
            contents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "text",
                        "text": "電影",
                        "size": "xl",
                        "align": "start",
                        "weight": "bold",
                        "color": "#000000"
                    }]
                },
                "hero": {
                    "type": "image",
                    "url": moviePoster[index],
                    "gravity": "top",
                    "size": "full",
                    "aspectRatio": "1:1.4",
                    "aspectMode": "cover",
                    "backgroundColor": "#FFFFFF"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [{
                        "type": "box",
                        "layout": "vertical",
                        "contents": [{
                            "type": "text",
                            "text": movieNameCN[index],
                            "margin": "none",
                            "size": "lg",
                            "align": "center",
                            "gravity": "top",
                            "weight": "bold"
                        },
                            {
                            "type": "text",
                            "text": movieNameEN[index],
                            "align": "center"
                        }]
                    },
                        {
                        "type": "separator",
                        "margin": "lg",
                        "color": "#FFFFFF"
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "上映日期："
                        },
                            {
                            "type": "text",
                            "text": movieReleaseTime[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                            "type": "text",
                            "text": "期待度：",
                            "align": "start",
                            "weight": "bold",
                            "color": "#BB21CA"
                        },
                            {
                            "type": "text",
                            "text": movieExpectation[index]
                        }]
                    },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [{
                                "type": "text",
                                "text": "滿意度：",
                                "align": "start",
                                "weight": "bold",
                                "color": "#2133CA"
                        },
                            {
                                "type": "text",
                                "text": movieSatisfactoryDegree[index],
                                "align": "start"
                        }]
                    }
                    ]},
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "詳細資料",
                            "text": "詳細資料",
                            "data": "postbackcontect"
                        },
                        "color": "#B0B0B0"
                    }]
                },
                "footer": {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "詳細資料",
                            "data": movieDetailUrl[index]
                        },
                        "color": "#B0B0B0"
                    }]
                }
            })
        # 回復
        flex_message = FlexSendMessage(
            alt_text='movielist',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )
    return(flex_message)


def use_movieurl_get_movieinfo(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)
        respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
        soup = BeautifulSoup(respData)

        # --------------------moviePoster
        moviePoster = soup.select_one(".movie_intro_foto img")["src"]
        moviePoster_message = ImageSendMessage(
            original_content_url=moviePoster,
            preview_image_url=moviePoster
        )
        # --------------------info
        movieNameCN = soup.select_one("h1").text
        movieNameEN = soup.select_one(".movie_intro_info_r h3").text
        movieTagStr = [i.text for i in soup.select(".level_name .gabtn")]
        movieTag = []
        for tag in movieTagStr:
            movieTag.append(tag.split()[0])
        movieReleaseTimeStr = [
            i.text for i in soup.select(".level_name_box+ span")]
        for date in movieReleaseTimeStr:
            movieReleaseTime = date[5:]
        movieRuntime = (soup.select_one("span:nth-child(6)").text)[5:]
        movieProCo = (soup.select("span:nth-child(7)")[1].text)[5:]
        movieIMDb = (soup.select_one("span:nth-child(8)").text)[7:]
        if movieIMDb == '':
            movieIMDb = '無評分'
        movieExpectation = (
            (soup.select(".evaluate_inner")[0].text).split())[-2]
        if movieExpectation == '':
            movieExpectation = '無評分'
        movieSatisfactoryDegree = (
            (soup.select(".evaluate_inner")[1].text).split())[3]
        if movieSatisfactoryDegree == '':
            movieSatisfactoryDegree = '無評分'

        # 彈性訊息
        movieTagContent = []
        for tag in movieTag:
            movieTagContent.append({
                "type": "text",
                "text": tag+'　　',
                "flex": 0,
                "weight": "bold",
                "color": "#000C3B"
            })
        info_flex_message = FlexSendMessage(
            alt_text='movielist',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "電影資訊",
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
                            "text": movieNameCN,
                            "size": "lg",
                            "align": "center",
                            "weight": "bold"
                        },
                        {
                            "type": "text",
                            "text": movieNameEN,
                            "size": "md",
                            "align": "center"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "contents": movieTagContent
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "上映日期",
                                    "weight": "bold"
                                },
                                {
                                    "type": "text",
                                    "text": movieReleaseTime
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
                                    "text": movieRuntime
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
                                    "text": movieProCo
                                }
                            ]
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "IMDb分數",
                                    "weight": "bold",
                                    "color": "#EAC44E"
                                },
                                {
                                    "type": "text",
                                    "text": movieIMDb
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
                                            "text": movieExpectation
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
                                            "text": movieSatisfactoryDegree
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            }
        )
        # --------------------story
        story = soup.select_one("#story")
        story_text_message = TextSendMessage(text=story)
        # --------------------actor
        actorName = [i.text for i in soup.select(".actor_inner h2")]
        actorContents = []
        if soup.select_one(".actor_inner h2") == None:
            actorContents.append({
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "無導演與演員資料",
                            "align": "center"
                        }
                    ]
                }
            })
        else:
            actorNameCN = []
            actorNameEN = []
            print(actorName)
            if len(actorName) > 0:
                for name in actorName:
                    name = name.split()
                    actorNameCN.append(name[0])
                    if len(name) >= 3:
                        ENname = ''
                        for index in range(len(name))[1:]:
                            ENname += ' '+name[index]
                        actorNameEN.append(ENname)
                    elif len(name) == 2:
                        actorNameEN.append(name[1])
                    else:
                        actorNameEN.append(' ')
                actorImg = [i["src"] for i in soup.select(
                    "._slickcontent .fotoinner img")]

            for index in range(len(actorNameCN)):
                actorContents.append({
                    "type": "bubble",
                    "direction": "ltr",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "導演及演員",
                                "size": "xl",
                                "align": "start",
                                "weight": "bold"
                            }
                        ]
                    },
                    "hero": {
                        "type": "image",
                        "url": actorImg[index],
                        "size": "full",
                        "aspectRatio": "3:4",
                        "aspectMode": "cover"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": actorNameCN[index],
                                "size": "xl",
                                "weight": "bold"
                            },
                            {
                                "type": "text",
                                "text": actorNameEN[index],
                                "size": "xl"
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
                                    "type": "uri",
                                    "label": "演員介紹",
                                    "uri": "https://linecorp.com"
                                }
                            }
                        ]
                    }
                })

        actor_flex_message = FlexSendMessage(
            alt_text='actorlist',
            contents={
                "type": "carousel",
                "contents": actorContents
            }
        )

        # --------------------movieStills
        movieStills = [i for i in soup.select(".imglist img")]
        movieStillsUrl = []
        for img in movieStills:
            movieStillsUrl.append(img["src"])

        movieStillsContent = []
        cnt = 0
        for img in movieStillsUrl:
            cnt += 1
            if cnt <= 10:
                movieStillsContent.append({
                    "type": "bubble",
                    "direction": "ltr",
                    "hero": {
                        "type": "image",
                        "url": img,
                        "size": "full",
                        "aspectRatio": "1.85:1",
                        "aspectMode": "cover"
                    }
                })

        movieStills_flex_message = FlexSendMessage(
            alt_text='movieStillslist',
            contents={
                "type": "carousel",
                "contents": movieStillsContent
            }
        )
        
        articleTitle = [i.text for i in soup.select("#native_ad_target h2")]
        articleContent = [i.text[21:-17]
                          for i in soup.select(".jq_text_overflow_link")]
        articleImg = [i['src'] for i in soup.select("#native_ad_target img")]
        articleURL = [i['href'] for i in soup.select("#native_ad_target li a")]

        articleContents = []
        for index in range(len((articleTitle))):
            articleContents.append({
                "type": "bubble",
                "direction": "ltr",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "相關文章",
                            "size": "xl",
                            "align": "start",
                            "weight": "bold"
                        }
                    ]
                },
                "hero": {
                    "type": "image",
                    "url": articleImg[index],
                    "size": "full",
                    "aspectRatio": "3:4",
                    "aspectMode": "cover"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": articleTitle[index],
                            "align": "center",
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": articleContent[index],
                            "size": "sm",
                            "wrap": True
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
                                "type": "uri",
                                "label": "詳全文（yahoo電影）",
                                "uri": articleURL[index]
                            }
                        }
                    ]
                }
            })

        article_flex_message = FlexSendMessage(
            alt_text='movieStillslist',
            contents={
                "type": "carousel",
                "contents": articleContents
            }
        )
        return(moviePoster_message, info_flex_message, story_text_message, actor_flex_message, movieStills_flex_message, article_flex_message)
        # --------------------
    except Exception as e:
        print(str(e))
