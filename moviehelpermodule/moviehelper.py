from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from linebot.models import *
import json
from moviehelpermodule.calculate import getDistance

def pagebox(soup):
    # --------------------pagebox
    if len(soup.select(".page_numbox ul")) == 0:
        pagebox_flex_message = FlexSendMessage(
            alt_text='pagebox',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "僅一頁搜尋結果",
                    "align": "center"
                    }
                ]
                }
            }
        )
    else:
        pagebox = soup.select(".page_numbox ul")[0]
        nowpage = pagebox.select(".active span")[0].text
        anotherpageURL = [i["href"] for i in pagebox.select("a")]
        anotherpage = [i.text for i in pagebox.select("a")]

        contents = []
        for index in range(len(anotherpage)):
            contents.append({
                "type": "text",
                "text": anotherpage[index],
                "align": "center",
                "action": {
                    "type": "postback",
                    "data": anotherpageURL[index]
                }
            })
        # 回復
        pagebox_flex_message = FlexSendMessage(
            alt_text='pagebox',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "目前第"+nowpage+"頁",
                    "align": "center"
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "xl",
                    "contents": contents
                    }
                ]
                }
            }
        )
    return(pagebox_flex_message)


def use_moviename_serch_movielist(movieNameOrURL, page):
    # 中文轉URL格式編碼
    if movieNameOrURL[:71] == 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=':
        movieURL = movieNameOrURL
    else:
        urlname = parse.quote(movieNameOrURL)
        movieURL = 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=' + \
            urlname + '&page=' + page
    # 電影清單URL
    print(movieURL)
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

    # --------------------movie list
    if soup.select_one(".release_movie_name > a") == None:
        movie_flex_message = FlexSendMessage(
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
                    "text": "找不到 "+movieNameOrURL+" 的相關電影",
                    "align": "center"
                    }
                ]
                }
            }
        )
        page = False
        return(movie_flex_message, page)
    else:
        movieInfo = [i.text for i in soup.select(".release_info")]
        movieNameCN = [i.text for i in soup.select(".release_movie_name > a")]
        movieNameEN = [i.text for i in soup.select(".en a")]
        movieExpectation = [i.text for i in soup.select("#content_l dt span")]
        movieSatisfactoryDegree = []
        for info in movieInfo:
            movieSatisfactoryDegree.append('未上映') if info.find(
                "滿意度") == -1 else movieSatisfactoryDegree.append(info[info.find("滿意度")+5:info.find("滿意度")+8])
        moviePoster = [i["src"] for i in soup.select(".release_foto img")]
        movieReleaseTime = [(i.text)[7:] for i in soup.select(".time")]
        movieDetailUrl = [i["href"]
                          for i in soup.select(".release_movie_name > a")]

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
                            "data": movieDetailUrl[index]
                        },
                        "color": "#B0B0B0"
                    }]
                }
            })
        # 回復
        movie_flex_message = FlexSendMessage(
            alt_text='movielist',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )

        pagebox_flex_message = pagebox(soup)

        return(movie_flex_message, pagebox_flex_message)


def use_moviename_serch_article(movieName):
    # --------------------article
    # 中文轉URL格式編碼
    urlname = parse.quote(movieName)
    # 電影清單URL
    movieURL = 'https://movies.yahoo.com.tw/tagged/'+urlname
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))
    soup = BeautifulSoup(respData, "html.parser")

    if soup.select_one(".fotoinner img") == None:
        article_flex_message = FlexSendMessage(
            alt_text='notfound',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "無找到 "+movieName+" 的相關文章",
                            "align": "center"
                        }
                    ]
                }
            }
        )
    else:
        articleTitle = [i.text for i in soup.select(".text_truncate_2")][:10]
        articleContent = [i.text[21:-17]
                          for i in soup.select(".jq_text_overflow_link")][:10]
        articleImg = [i['src'] for i in soup.select("#content_l img")][:10]
        articleURL = [i['href'] for i in soup.select(".news_content a")][:10]
        articleDate = [i.text for i in soup.select(".day")][:10]

        articleContents = []
        for index in range(len(articleTitle)):
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
            alt_text='articlelist',
            contents={
                "type": "carousel",
                "contents": articleContents
            }
        )
    return(article_flex_message)


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
        moviePoster_image_message = ImageSendMessage(
            original_content_url=moviePoster,
            preview_image_url=moviePoster
        )
        # --------------------info
        movieNameCN = soup.select_one("h1").text
        movieNameEN = soup.select_one(".movie_intro_info_r h3").text
        movieTag = [((i.text.split())[0])+'　'
                    for i in soup.select(".level_name .gabtn")]
        movieReleaseTime = soup.select_one(".level_name_box+ span").text[5:]
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
        director = [i.text.replace('\n', '').replace(' ', '').split(
            '、') for i in soup.select(".movie_intro_list")][0]
        director = ','.join(director)
        actor = [i.text.replace('\n', '').replace(' ', '').split(
            '、') for i in soup.select(".movie_intro_list")][1]
        actor = ','.join(actor)
        # 彈性訊息
        movieTagContent = []
        for tag in movieTag:
            movieTagContent.append({
                "type": "text",
                "text": tag,
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
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "導演",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "text",
                                            "text": director,
                                            "size": "xs",
                                            "wrap": True
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "演員",
                                                    "weight": "bold"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": actor,
                                                    "size": "xxs",
                                                    "wrap": True
                                                }
                                            ]
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
        for br in story.select('br'):
            br.insert_after("\n")
            br.unwrap()
        story = story.text
        story_flex_message = FlexSendMessage(
            alt_text='actorlist',
            contents={
                "type": "bubble",
                "direction": "ltr",
                "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "電影簡介",
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
                    "text": story,
                    "align": "start",
                    "wrap": True
                    }
                ]
                }
        })
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
                actorNameCN = actorNameCN[:10]
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
            else:
                break

        movieStills_flex_message = FlexSendMessage(
            alt_text='movieStillslist',
            contents={
                "type": "carousel",
                "contents": movieStillsContent
            }
        )

        return(moviePoster_image_message, info_flex_message, story_flex_message, actor_flex_message, movieStills_flex_message)
        # --------------------
    except Exception as e:
        print(str(e))


def search_movie_thisweekAndIntheaters(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)
        respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
        soup = BeautifulSoup(respData)

        # --------------------info
        movieNameCN = [i.text.strip()
                                    for i in soup.select(".release_movie_name > a")]
        movieNameEN = [i.text.strip() for i in soup.select(".en a")]
        movieInfo = [i for i in soup.select(".release_movie_name")]
        movieExpectation = []
        movieSatisfactoryDegree = []
        for html in movieInfo:
            movieExpectation.append(html.select("span")[0].text)
            try:
                movieSatisfactoryDegree.append(
                    (html.select("span")[1])["data-num"])
            except:
                movieSatisfactoryDegree.append("無資料")
        moviePoster = [i["src"] for i in soup.select(".release_foto img")]
        movieReleaseTime = [(i.text)[7:]
                             for i in soup.select(".release_movie_time")]
        movieDetailUrl = [i["href"]
                            for i in soup.select(".release_movie_name > a")]
        # --------------------
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
                            "data": movieDetailUrl[index]
                        },
                        "color": "#B0B0B0"
                    }]
                }
            })
        # 回復
        movie_flex_message = FlexSendMessage(
            alt_text='movielist',
            contents={
                "type": "carousel",
                "contents": contents
            }
        )

        pagebox_flex_message = pagebox(soup)

        return(movie_flex_message, pagebox_flex_message)
    except Exception as e:
        print(str(e))


def search_movie_comingsoon(url):
    if url == '':
        url = 'https://movies.yahoo.com.tw/movie_comingsoon.html'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    # --------------------movieTab

    movieTab = [i for i in soup.select(".comingsoon_tab li")]
    contents = []
    for tab in movieTab:
        print(tab)
        if (tab.text)[:2] == '20':  # 年
            print(tab.text)
            contents.append({
                "type": "text",
                "text": tab.text,
                "size": "lg",
                "align": "center",
                "weight": "bold"
            })
        else:
            if tab["class"] == ['select']:  # 當月
                print(True)
                contents.append({
                    "type": "text",
                    "text": tab.text,
                    "size": "xxl",
                    "action": {
                        "type": "postback",
                        "data": tab.a["href"]
                    }
                })
            else:
                print(tab.text)  # 每月
                print(tab.a["href"])
                contents.append({
                    "type": "text",
                    "text": tab.text,
                    "size": "xl",
                    "weight": "bold",
                    "action": {
                        "type": "postback",
                        "data": tab.a["href"]
                    }
                })

    movietab_flex_message = FlexSendMessage(
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
                "text": "即將上映",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contents
            }
        }
    )

    # --------------------movieInfo
    movieInfo = [i.text for i in soup.select(".release_info")]
    movieNameCN = [i.text.strip()
                                for i in soup.select(".release_movie_name > a")]
    movieNameEN = [i.text.strip() for i in soup.select(".en a")]
    movieExpectation = [i.text for i in soup.select("#content_l dt span")]
    movieSatisfactoryDegree = []
    for info in movieInfo:
        movieSatisfactoryDegree.append('未上映') if info.find(
            "滿意度") == -1 else movieSatisfactoryDegree.append(info[info.find("滿意度")+5:info.find("滿意度")+8])
    moviePoster = [i["src"] for i in soup.select(".release_foto img")]
    movieReleaseTime = [(i.text)[7:]
                         for i in soup.select(".release_movie_time")]
    movieDetailUrl = [i["href"]
                        for i in soup.select(".release_movie_name > a")]

    # --------------------
    contents = []
    if movieNameCN == []:
            contents.append({
                "type": "bubble",
                "direction": "ltr",
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "無即將上映的電影",
                    "size": "lg",
                    "align": "center"
                    }
                ]
                }
            })
    else:
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
                            "data": movieDetailUrl[index]
                        },
                        "color": "#B0B0B0"
                    }]
                }
            })

    # 回復
    movie_flex_message = FlexSendMessage(
        alt_text='movielist',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )

    pagebox_flex_message = pagebox(soup)

    return(movietab_flex_message, movie_flex_message, pagebox_flex_message)


def search_movie_chart(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    movieRank = [i.text for i in soup.select(".tr+ .tr .td:nth-child(1)")]
    movieRankTypeDiv = [i for i in soup.select(".up , .new , .down")]
    movieRankType = []
    for div in movieRankTypeDiv:
        if div["class"][1] == "new":
            movieRankType.append("🆕")
        if div["class"][1] == "up":
            movieRankType.append("🔼")
        if div["class"][1] == "down":
            movieRankType.append("🔽")
    movieRankOneImg = (soup.select_one(".rank_list_box img"))["src"]
    movieNameCN = ['　'+i.text for i in soup.select(".rank_txt , h2")]
    movieNameEN = soup.select_one("h3").text
    movieReleaseTime = [
        '　'+i.text for i in soup.select(".tr+ .tr .td:nth-child(5)")]
    movieSatisfactoryDegree = [i.text.strip()
                                            for i in soup.select(".starwithnum")]
    movieURLHTML = [i for i in soup.select(
        ".up~ .td:nth-child(4) , .down~ .td:nth-child(4) , .new~ .td:nth-child(4)")]
    movieURL = []
    for html in movieURLHTML:
        if html.a != None:
            movieURL.append(html.a["href"])
        else:
            movieURL.append("沒有資料")
    rankcontents = []
    for index in range(len(movieRank)):
        if index == 0:
            rankcontents.append({
                "type": "box",
                "layout": "vertical",
                "action": {
                    "type": "postback",
                    "data": movieURL[index]
                },
                "contents": [
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRank[index],
                        "flex": 0,
                        "align": "start"
                        },
                        {
                        "type": "text",
                        "text": movieRankType[index],
                        "flex": 0,
                        "align": "start"
                        },
                        {
                        "type": "text",
                        "text": '　'+movieReleaseTime[index],
                        "flex": 0
                        },
                        {
                        "type": "text",
                        "text": movieSatisfactoryDegree[index]+int(float(movieSatisfactoryDegree[index]))*'★',
                        "flex": 0
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "image",
                        "url": movieRankOneImg,
                        "flex": 0
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "spacer",
                            "size": "xxl"
                            },
                            {
                            "type": "text",
                            "text": movieNameCN[index],
                            "size": "lg",
                            "align": "start",
                            "gravity": "center",
                            "weight": "bold",
                            "wrap": True
                            },
                            {
                            "type": "text",
                            "text": movieNameEN,
                            "align": "start",
                            "gravity": "center",
                            "wrap": True
                            }
                        ]
                        }
                    ]
                    }
                ]
            })
        else:
            rankcontents.append({
                "type": "box",
                "layout": "vertical",
                "margin": "lg",
                "action": {
                    "type": "postback",
                    "data": movieURL[index]
                },
                "contents": [
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": '{:>2}'.format(movieRank[index]),
                        "flex": 0,
                        "align": "start",
                        "gravity": "bottom"
                        },
                        {
                        "type": "text",
                        "text": movieNameCN[index],
                        "size": "lg",
                        "align": "start",
                        "gravity": "center",
                        "weight": "bold",
                        "wrap": True
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRankType[index],
                        "flex": 0,
                        "align": "start"
                        },
                        {
                        "type": "text",
                        "text": movieReleaseTime[index],
                        "flex": 1
                        },
                        {
                        "type": "text",
                        "text": movieSatisfactoryDegree[index]+int(float(movieSatisfactoryDegree[index]))*'★',
                        "flex": 0
                        }
                    ]
                    }
                ]
            })

    movierank_flex_message = FlexSendMessage(
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
                "text": "排行榜",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": rankcontents[:15]
            }
        }
    )

    return(movierank_flex_message)


def select_movie_type():
    '''
    1動作
    2冒險
    3科幻
    4奇幻
    5劇情
    6犯罪
    7恐怖
    8懸疑驚悚
    9喜劇
    10愛情
    11溫馨家庭
    12動畫
    13戰爭
    14音樂歌舞
    15歷史傳記
    16紀錄片
    17勵志
    18武俠
    19影展
    20戲劇
    21影集
    '''
    movieType_flex_message = FlexSendMessage(
        alt_text='typelist',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "類型找電影",
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
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "動作",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "動作"
                    }
                    },
                    {
                    "type": "text",
                    "text": "冒險",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "冒險"
                    }
                    },
                    {
                    "type": "text",
                    "text": "科幻",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "科幻"
                    }
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
                    "text": "奇幻",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "奇幻"
                    }
                    },
                    {
                    "type": "text",
                    "text": "劇情",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "劇情"
                    }
                    },
                    {
                    "type": "text",
                    "text": "犯罪",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "犯罪"
                    }
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
                    "text": "恐怖",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "恐怖"
                    }
                    },
                    {
                    "type": "text",
                    "text": "懸疑驚悚",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "懸疑驚悚"
                    }
                    },
                    {
                    "type": "text",
                    "text": "喜劇",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "喜劇"
                    }
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
                    "text": "愛情",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "愛情"
                    }
                    },
                    {
                    "type": "text",
                    "text": "溫馨家庭",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "溫馨家庭"
                    }
                    },
                    {
                    "type": "text",
                    "text": "動畫",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "動畫"
                    }
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
                    "text": "戰爭",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "戰爭"
                    }
                    },
                    {
                    "type": "text",
                    "text": "音樂歌舞",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "音樂歌舞"
                    }
                    },
                    {
                    "type": "text",
                    "text": "歷史傳記",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "歷史傳記"
                    }
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
                    "text": "紀錄片",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "紀錄片"
                    }
                    },
                    {
                    "type": "text",
                    "text": "勵志",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "勵志"
                    }
                    },
                    {
                    "type": "text",
                    "text": "武俠",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "武俠"
                    }
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
                    "text": "影展",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "影展"
                    }
                    },
                    {
                    "type": "text",
                    "text": "戲劇",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "戲劇"
                    }
                    },
                    {
                    "type": "text",
                    "text": "影集",
                    "size": "lg",
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "影集"
                    }
                    }
                ]
                }
            ]
            }
        }
    )

    return(movieType_flex_message)


def search_movie_type(typeName, url):
    if typeName == '':
        movieURL = url
    else:
        movieTypeDition = {
            "1": "動作",
            "2": "冒險",
            "3": "科幻",
            "4": "奇幻",
            "5": "劇情",
            "6": "犯罪",
            "7": "恐怖",
            "8": "懸疑驚悚",
            "9": "喜劇",
            "10": "愛情",
            "11": "溫馨家庭",
            "12": "動畫",
            "13": "戰爭",
            "14": "音樂歌舞",
            "15": "歷史傳記",
            "16": "紀錄片",
            "17": "勵志",
            "18": "武俠",
            "19": "影展",
            "20": "戲劇",
            "21": "影集",
        }
        typeNo = list(movieTypeDition.keys())[
                      list(movieTypeDition.values()).index(typeName)]
        # 電影清單URL
        movieURL = 'https://movies.yahoo.com.tw/moviegenre_result.html?genre_id='+typeNo+'&page=1'

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(movieURL, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))
    soup = BeautifulSoup(respData, "html.parser")

    movieNameCN = [i.text.strip()
                                for i in soup.select(".release_movie_name > .gabtn")]
    movieNameEN = [i.text.strip() for i in soup.select(".en .gabtn")]
    movieInfo = [i for i in soup.select(".release_movie_name")]
    movieExpectation = []
    movieSatisfactoryDegree = []
    for html in movieInfo:
        movieExpectation.append(html.select("span")[0].text)
        try:
            movieSatisfactoryDegree.append(
                (html.select("span")[1])["data-num"])
        except:
            movieSatisfactoryDegree.append("無資料")
    moviePoster = [i["src"] for i in soup.select("#content_l img")]
    movieReleaseTime = [(i.text)[7:]
                         for i in soup.select(".release_movie_time")]
    movieDetailUrl = [i["href"]
                        for i in soup.select(".release_movie_name > .gabtn")]
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
                        "data": movieDetailUrl[index]
                    },
                    "color": "#B0B0B0"
                }]
            }
        })
    # 回復
    movie_flex_message = FlexSendMessage(
        alt_text='movielist',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )

    pagebox_flex_message = pagebox(soup)

    return(movie_flex_message, pagebox_flex_message)


def use_location_search_movietheater(userAddress, userLat, userLng):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+str(userLat)+','+str(userLng)+'&radius=5000&keyword=movietheater&key=AIzaSyATyj-s1QtmrmCFQIsDhnPxS4-D929PlxM&language=zh-TW'
    print(url)
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    jsondata = json.loads(respData)
    movietheaterName = []
    movietheaterLat = []
    movietheaterLng = []
    movietheaterPhotos = []
    movietheaterRating = []
    movietheaterAddress = []
    for data in jsondata["results"]:
        movietheaterName.append(data["name"])
        movietheaterLat.append(data["geometry"]["location"]["lat"])
        movietheaterLng.append(data["geometry"]["location"]["lng"])
        try:
            photoReference = data["photos"][0]['photo_reference']
            movietheaterPhotos.append('https://maps.googleapis.com/maps/api/place/photo?maxheight=900&maxwidth=1200&photoreference=' +
                                      photoReference+'&key=AIzaSyATyj-s1QtmrmCFQIsDhnPxS4-D929PlxM')
        except:
            movietheaterPhotos.append('https://i.imgur.com/CMAl4DQ.jpg')
        movietheaterRating.append(data["rating"])
        movietheaterAddress.append(data["vicinity"])
    print(movietheaterName[1])
    print(movietheaterLat[1])
    print(movietheaterLng[1])
    print(movietheaterPhotos[1])
    print(movietheaterRating[1])
    print(movietheaterAddress[1])
    print(getDistance(25.04179847198162,121.525639358062,movietheaterLat[0],movietheaterLng[0]))
    contents = []
    for index in range(len(movietheaterName[:10])):
        contents.append({
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movietheaterName[index],
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "hero": {
            "type": "image",
            "url": movietheaterPhotos[index],
            "size": "full",
            "aspectRatio": "4:3",
            "aspectMode": "fit"
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": movietheaterName[index],
                "align": "start"
                },
                {
                "type": "text",
                "text": movietheaterAddress[index]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "評價",
                    "flex": 0,
                    "gravity": "bottom"
                    },
                    {
                    "type": "text",
                    "text": movietheaterRating[index],
                    "size": "xl"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "距離",
                    "flex": 0,
                    "gravity": "bottom"
                    },
                    {
                    "type": "text",
                    "text": Distance(userLat,userLng,movietheaterLat[index],movietheaterLng[index]),
                    "flex": 0,
                    "size": "xl"
                    },
                    {
                    "type": "text",
                    "text": "公里",
                    "align": "start",
                    "gravity": "bottom"
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
                    "type": "uri",
                    "label": "上映場次",
                    "uri": "https://linecorp.com"
                }
                },
                {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "位置資訊",
                    "uri": "https://linecorp.com"
                }
                }
            ]
            }
        })
    movietheater_flex_message = FlexSendMessage(
        alt_text='movietheater',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )
    return(movietheater_flex_message)

def workTeam():
    workTeam_flex_message = FlexSendMessage(
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
                "text": "製作者名單",
                "size": "xl",
                "align": "center",
                "weight": "bold"
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xl",
                "contents": [
                    {
                    "type": "text",
                    "text": "構想：",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "林萬豪",
                    "align": "start"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "程式設計：",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "林萬豪",
                    "align": "start"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "前端介面：",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "林萬豪",
                    "align": "start"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                    {
                    "type": "text",
                    "text": "畫面插圖：",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "陳衍儒(還沒畫)",
                    "align": "start"
                    }
                ]
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "xl",
                "contents": [
                    {
                    "type": "text",
                    "text": "資料來源：",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": "Yahoo電影",
                    "align": "start"
                    }
                ]
                }
            ]
            }
        }
    )
    return(workTeam_flex_message)
