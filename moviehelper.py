from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from linebot.models import *

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

def use_moviename_serch_movielist(movieName, page):
    # 中文轉URL格式編碼
    print(movieName)
    if movieName[:71] == 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=':
        movieURL = movieName
    else:
        urlname = parse.quote(movieName)
        movieURL = 'https://movies.yahoo.com.tw/moviesearch_result.html?type=movie&keyword=' + urlname + '&page=' + page
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
                            "text": "無找到 "+movieName+" 的相關電影",
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


def search_movie_thisweek(url, page):
    try:
        url = url+page
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
        req = request.Request(url, headers=headers)
        resp = request.urlopen(req)
        respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
        soup = BeautifulSoup(respData)

        # --------------------info
        movieInfo = [i.text for i in soup.select(".release_info")]
        movieNameCN = [i.text.strip() for i in soup.select(".release_movie_name > a")]
        movieNameEN = [i.text.strip() for i in soup.select(".en a")]
        movieExpectation = [i.text for i in soup.select("#content_l dt span")]
        movieSatisfactoryDegree = []
        for info in movieInfo:
            movieSatisfactoryDegree.append('未上映') if info.find(
                "滿意度") == -1 else movieSatisfactoryDegree.append(info[info.find("滿意度")+5:info.find("滿意度")+8])
        moviePoster = [i["src"] for i in soup.select(".release_foto img")]
        movieReleaseTime = [(i.text)[7:] for i in soup.select(".release_movie_time")]
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