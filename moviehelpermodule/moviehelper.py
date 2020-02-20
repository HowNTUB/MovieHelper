from urllib import request, parse
import urllib
from bs4 import BeautifulSoup
from linebot.models import *
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
        if soup.select(".movie_intro_list")[0] == None:
            director="無導演資訊"
        else:
            director = [i.text.replace('\n', '').replace(' ', '').split(
                '、') for i in soup.select(".movie_intro_list")][0]
            director = ','.join(director)
        if soup.select(".movie_intro_list")[0] == None:
            director="無演員資訊"
        else:
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
                            "weight": "bold",
                            "wrap": True
                        },
                        {
                            "type": "text",
                            "text": movieNameEN,
                            "size": "md",
                            "align": "center",
                            "wrap": True
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
            actorDetailURL = []
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
                actorDetailURL = [i["href"] for i in soup.select(".starlist a")]
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
                                    "type": "postback",
                                    "label": "詳細介紹",
                                    "data": actorDetailURL[index]
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

def use_actorURL_get_actorIntorduction(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    # --------------------info
    actorNameCN = soup.select_one(".maker_name").text
    actorNameEN = soup.select_one(".name_en").text
    actorNameCN = actorNameCN[:-len(actorNameEN)]
    actorBirth = soup.select_one(".maker_birth").text[5:]
    actorImg = soup.select_one(".pic img")["src"]
    actorImgFrom = soup.select_one(".pic_txt").text
    actorTitle = [i.text.split() for i in soup.select(".maker_tips")][0]
    actorPop = soup.select_one(".popnum").text[3:]
    actorIntorduction = soup.select_one(".jq_text_overflow_href_main").text

    titleContent=[]
    for title in actorTitle:
        titleContent.append({
            "type": "text",
            "text": title,
            "flex": 0,
            "weight": "bold",
            "color": "#000C3B"
        })

    actor_flex_message = FlexSendMessage(
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
                "text": "人物資訊",
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
                "contents": [
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "image",
                        "url": actorImg,
                        "align": "start",
                        "aspectRatio": "1:2",
                        "aspectMode": "cover"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "text",
                            "text": actorNameCN,
                            "size": "lg",
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": actorNameEN
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "horizontal",
                        "flex": 0,
                        "spacing": "md",
                        "margin": "lg",
                        "contents": titleContent
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                            "type": "text",
                            "text": "生日：",
                            "flex": 0,
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": actorBirth
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "margin": "lg",
                        "contents": [
                            {
                            "type": "text",
                            "text": "人氣：",
                            "flex": 0,
                            "weight": "bold"
                            },
                            {
                            "type": "text",
                            "text": actorPop
                            }
                        ]
                        }
                    ]
                    }
                ]
                },
                {
                    "type": "text",
                    "text": actorImgFrom,
                    "margin": "md",
                    "size": "xxs",
                    "align": "end",
                    "color": "#6A6A6A"
                }
            ]
            }
        }
    )

    introductionlist_flex_message = FlexSendMessage(
        alt_text='introductionlist',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "button",
                "action": {
                    "type": "message",
                    "label": "個人簡介",
                    "text": 'actorIntorduction'
                }
                },
                {
                "type": "separator"
                },
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "導演作品",
                    "data": 'https://movies.yahoo.com.tw/name_movies/'+url[url.find('-',-10)+1:]+'?type=1'
                }
                },
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "演員作品",
                    "data": 'https://movies.yahoo.com.tw/name_movies/'+url[url.find('-',-10)+1:]+'?type=2'
                }
                },
                {
                "type": "separator"
                },
                {
                "type": "button",
                "action": {
                    "type": "postback",
                    "label": "相關文章",
                    "data": 'https://movies.yahoo.com.tw/tagged/'+actorNameCN
                }
                }
            ]
            }
        }
    )

    return(actor_flex_message, introductionlist_flex_message)

def use_actorURL_search_movielist(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    # movieNameCN 中文名
    # movieNameEN 英文名
    # movieExpectation 期待值
    # movieSatisfactoryDegree 滿意度
    # moviePoster 海報
    # movieReleaseTime 上映時間
    # movieDetailUrl 詳細資訊網址

    # --------------------movie list
    if soup.select_one(".release_movie_name > .gabtn") == None:
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
                    "text": "找不到的相關電影",
                    "align": "center"
                    }
                ]
                }
            }
        )
        page = False
        return(movie_flex_message, page)
    else:
        movieInfo = [i for i in soup.select(".release_info")]
        movieInfoText = [i.text for i in soup.select(".release_info")]
        movieNameCN = [i.text.strip() for i in soup.select(".release_movie_name > .gabtn")]
        movieNameEN = []
        for i in soup.select(".en .gabtn"):
            if i.text.strip() == '':
                movieNameEN.append(' ')
            else:
                movieNameEN.append(i.text.strip())
        movieExpectation = []
        for info in movieInfoText:
            movieExpectation.append('未上映') if info.find(
                "期待度") == -1 else movieExpectation.append(info[info.find("期待度")+5:info.find("期待度")+8])
        movieSatisfactoryDegree = []
        if url[-1] == '1':
            for html in movieInfo:
                try:#沒期待度
                    movieSatisfactoryDegree.append(
                        (html.select("span")[0])["data-num"])
                except:#有期待度
                    movieSatisfactoryDegree.append(
                        (html.select("span")[1])["data-num"])
        elif url[-1] == '2':
            for html in movieInfo:
                if html.select(".count") == []:
                    movieSatisfactoryDegree.append("未上映")
                else:
                    movieSatisfactoryDegree.append(
                        (html.select(".count")[0])["data-num"])
        
        moviePoster = [i["src"] for i in soup.select("#content_l img")]
        movieReleaseTime = [(i.text)[7:] for i in soup.select(".release_movie_time")]
        movieDetailUrl = [i["href"]
                            for i in soup.select(".release_movie_name > .gabtn")]
        print(movieNameCN)
        print(movieNameEN)
        print(movieExpectation)
        print(movieSatisfactoryDegree)
        print(moviePoster)
        print(movieReleaseTime)
        print(movieDetailUrl)
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

def search_movie_thisweekAndIntheaters(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    # --------------------info
    movieInfo = [i for i in soup.select(".release_info")]
    movieInfoText = [i.text for i in soup.select(".release_info")]
    movieNameCN = [i.text.strip() for i in soup.select(".release_movie_name > .gabtn")]
    movieNameEN = [i.text.strip() for i in soup.select(".en .gabtn")]
    movieExpectation = []
    for info in movieInfoText:
        movieExpectation.append('未上映') if info.find(
            "期待度") == -1 else movieExpectation.append(info[info.find("期待度")+5:info.find("期待度")+8])
    movieSatisfactoryDegree = []
    for html in movieInfo:
        try:#沒期待度
            movieSatisfactoryDegree.append(
                (html.select("span")[0])["data-num"])
        except:#有期待度
            movieSatisfactoryDegree.append(
                (html.select("span")[1])["data-num"])
    moviePoster = [i["src"] for i in soup.select("#content_l img")]
    movieReleaseTime = [(i.text)[7:] for i in soup.select(".release_movie_time")]
    movieDetailUrl = [i["href"]
                        for i in soup.select(".release_movie_name > .gabtn")]
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
                    "spacing": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRank[index],
                        "flex": 0
                        },
                        {
                        "type": "text",
                        "text": movieRankType[index],
                        "flex": 0
                        },
                        {
                        "type": "text",
                        "text": movieReleaseTime[index],
                        "flex": 1
                        },
                        {
                        "type": "text",
                        "text": movieSatisfactoryDegree[index]+int(float(movieSatisfactoryDegree[index]))*'★',
                        "flex": 0,
                        "align": "end"
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
                        "align": "start"
                        },
                        {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                            "type": "spacer",
                            "size": "lg"
                            },
                            {
                            "type": "text",
                            "text": movieNameCN[index],
                            "size": "lg",
                            "align": "start",
                            "weight": "bold",
                            "wrap": True
                            },
                            {
                            "type": "text",
                            "text": movieNameEN,
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
                "margin": "md",
                "action": {
                    "type": "postback",
                    "data": movieURL[index]
                },
                "contents": [
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRank[index],
                        "flex": 0,
                        "gravity": "bottom"
                        },
                        {
                        "type": "text",
                        "text": movieNameCN[index],
                        "flex": 0,
                        "size": "lg",
                        "weight": "bold"
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "horizontal",
                    "spacing": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movieRankType[index],
                        "flex": 0
                        },
                        {
                        "type": "text",
                        "text": movieReleaseTime[index],
                        "flex": 1
                        },
                        {
                        "type": "text",
                        "text": movieSatisfactoryDegree[index],
                        "flex": 0
                        },
                        {
                        "type": "text",
                        "text": int(float(movieSatisfactoryDegree[index]))*'★',
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

def get_location_message():
    location_flex_message = FlexSendMessage(
        alt_text='getLocation',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "點擊地圖的指定位置，我將幫您查詢附近的電影院。",
                "align": "start",
                "wrap": True
                },
                {
                "type": "separator",
                "margin": "xl"
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
                    "type":"location",
                    "label": "選擇指定位置"
                }
                }
            ]
            }
        }
    )
    return(location_flex_message)
def use_location_search_movietheater(userAddress, userLat, userLng):
    import googlemaps
    import os
    os.environ['http_proxy'] = os.environ['QUOTAGUARD_URL']

    googleAPIKey = os.environ['GOOGLE_API_KEY'] # 在heroku專案中的Config Vars中設定
    gmaps = googlemaps.Client(key=googleAPIKey)
    nearbyMovietheater = googlemaps.places.places_nearby(location=(userLat,userLng), radius=50000, language="zh-TW", keyword="movietheater", client=gmaps)
    print(nearbyMovietheater)
    movietheaterName = []
    movietheaterLat = []
    movietheaterLng = []
    movietheaterPhotos = []
    movietheaterRating = []
    movietheaterAddress = []
    for data in nearbyMovietheater["results"]:
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
    contents = []
    for index in range(len(movietheaterName)):
        print(index)
        print(movietheaterName[index])
        print(movietheaterLat[index])
        print(movietheaterLng[index])
        print(movietheaterPhotos[index])
        print(movietheaterRating[index])
        print(movietheaterAddress[index])
        print(getDistance(userLat,userLng,movietheaterLat[index],movietheaterLng[index]))
        if index > 9 : break
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
                    "text": str(movietheaterRating[index]),
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
                    "text": str(getDistance(userLat,userLng,movietheaterLat[index],movietheaterLng[index])),
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

    print(movietheaterName)
    print(movietheaterLat)
    print(movietheaterLng)
    print(movietheaterPhotos)
    print(movietheaterRating)
    print(movietheaterAddress)
    movietheater_flex_message = FlexSendMessage(
        alt_text='movietheater',
        contents={
            "type": "carousel",
            "contents": contents
        }
    )
    return(movietheater_flex_message)
    
def get_MovieMoment(page):
    url = 'http://www.atmovies.com.tw/movie/new/'
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)
    movieOption = [i for i in soup.select("form:nth-child(3) select option")][1:]
    movieName = []
    movieID = []
    for option in movieOption:
        movieName.append(option.text)
        movieID.append(option["value"][33:-1])
    movieNameContents = []
    for index in range((int(page)-1)*15,int(page)*15):
        movieNameContents.append({
            "type": "box",
            "layout": "vertical",
            "margin": "md",
            "action": {
                "type": "postback",
                "data": "電影時刻"+movieID[index]+"/a02/,1"
            },
            "contents": [
                {
                "type": "text",
                "text": movieName[index],
                "size": "lg"
                },
                {
                "type": "separator",
                "margin": "md"
                }
            ]
        })
    movieSelect_flex_message = FlexSendMessage(
        alt_text='movieSelect',
        contents={
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "上映中的電影",
                "size": "xl",
                "align": "start",
                "weight": "bold"
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": movieNameContents
            }
        }
    )
    
    totalPage = int(len(movieName)/15)
    nowPage = int(page)
    contents = []
    for index in range(totalPage):
        contents.append({
            "type": "text",
            "text": str(index+1),
            "align": "center",
            "action": {
                "type": "postback",
                "data": "電影表"+str(index+1)
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
                "text": "目前第"+str(nowPage)+"頁",
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
    return(movieSelect_flex_message, pagebox_flex_message)

def use_movieurl_get_movieMoment(movieID, inAreaID, page):
    import time
    url = 'http://www.atmovies.com.tw/showtime/'+movieID+inAreaID
    print(url)
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'
    req = request.Request(url, headers=headers)
    resp = request.urlopen(req)
    respData = str(resp.read().decode('utf-8'))  # 將所得的資料解碼
    soup = BeautifulSoup(respData)

    areaOption = [i for i in soup.select(".theaterSelect select option")][1:]
    print(areaOption)
    areaMessageContents = []
    areaContent = []
    for area in areaOption:
        print(area)
        areaName = area.text.strip()
        areaID = area["value"][-5:]
        areaContent.append({
          "type": "button",
          "action": {
            "type": "postback",
            "label": areaName,
            "data": "電影時刻"+movieID+areaID+","+"1"
          }
        })
    for contentIndex in range(int(len(area)/4)):
        contentsAreaContent = []
        for areaIndex in range(4):
            contentsAreaContent.append(areaContent[contentIndex*4+areaIndex])
        areaMessageContents.append({
            "type": "bubble",
            "direction": "ltr",
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": contentsAreaContent
            }
        })

    area_flex_message = FlexSendMessage(
        alt_text='areaSelect',
        contents={
            "type": "carousel",
            "contents": areaMessageContents
        }
    )
    
    movietheaterData = [i.text.strip() for i in soup.select("#filmShowtimeBlock ul")]
    movietheaterContents = []
    for content in movietheaterData[(int(page)-1)*10:int(page)*10]:
        print(content.split())
        print("="*10)
        timeContents = []
        for movietime in (content.split())[1:]:
            print(movietime)
            now=time.strftime("%H:%M", time.localtime(time.time()+28800))
            print(now)
            number = ['1','2','3','4','5','6','7','8','9','0']
            if movietime[-1] in number:
                if int(now[:2])>=int(movietime[:2]):
                    if int(now[3:])>int(movietime[3:]):
                        timeContents.append({
                            "type": "box",
                            "layout": "vertical",
                            "margin": "md",
                            "action": {
                                "type": "postback",
                                "data": "這裡放URL"
                            },
                            "contents": [
                                {
                                "type": "text",
                                "text": movietime,
                                "size": "lg",
                                "align": "center",
                                "color": "#C1C1C1"
                                },
                                {
                                "type": "separator",
                                "margin": "md"
                                }
                            ]
                        })
                else:
                    timeContents.append({
                        "type": "box",
                        "layout": "vertical",
                        "margin": "md",
                        "action": {
                            "type": "postback",
                            "data": "這裡放URL"
                        },
                        "contents": [
                            {
                            "type": "text",
                            "text": movietime,
                            "size": "lg",
                            "align": "center"
                            },
                            {
                            "type": "separator",
                            "margin": "md"
                            }
                        ]
                    })
            else:
                timeContents.append({
                    "type": "box",
                    "layout": "vertical",
                    "margin": "md",
                    "contents": [
                        {
                        "type": "text",
                        "text": movietime,
                        "size": "lg",
                        "align": "center"
                        },
                        {
                        "type": "separator",
                        "margin": "md"
                        }
                    ]
                })
        movietheaterContents.append({
            "type": "bubble",
            "direction": "ltr",
            "header": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": content.split()[0],
                "size": "xl",
                "align": "start",
                "weight": "bold",
                "wrap": True
                }
            ]
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": timeContents
            }
        })

    movietheater_flex_message = FlexSendMessage(
        alt_text='articlelist',
        contents={
            "type": "carousel",
            "contents": movietheaterContents
        }
    )

    totalPage = int(len(movietheaterData)/10)
    print(totalPage)
    if totalPage>0 :
        nowPage = int(page)
        print(nowPage)
        contents = []
        for index in range(totalPage):
            if index != nowPage:
                contents.append({
                    "type": "text",
                    "text": str(index+1),
                    "align": "center",
                    "action": {
                        "type": "postback",
                        "data": "電影時刻"+movieID+"/"+inAreaID+"/,"+str(index+1)
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
                    "text": "目前第"+str(nowPage)+"頁",
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
    else:
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

    movieName = soup.select_one("h2 a").text
    movieNameCN = movieName[:movieName.find(" ")]
    movieNameEN = movieName[movieName.find(" ")+1:]
    movieDetail = soup.select_one(".runtimeText").text
    movieRuntime = movieDetail[movieDetail.find("片長：")+3:movieDetail.find("分")+1]
    movieReleaseTime = movieDetail[movieDetail.find("上映日期：")+5:movieDetail.find("廳數")+-1]
    movieInfo_flex_message = FlexSendMessage(
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
                "text": movieNameCN,
                "size": "md",
                "align": "center",
                "weight": "bold",
                "wrap": True
                },
                {
                "type": "text",
                "text": movieNameEN,
                "size": "sm",
                "align": "center",
                "wrap": True
                },
                {
                "type": "box",
                "layout": "horizontal",
                "margin": "lg",
                "contents": [
                    {
                    "type": "text",
                    "text": "片長：",
                    "align": "end"
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
                "contents": [
                    {
                    "type": "text",
                    "text": "上映日期：",
                    "align": "end"
                    },
                    {
                    "type": "text",
                    "text": movieReleaseTime
                    }
                ]
                },
                {
                "type": "separator",
                "margin": "xl"
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
                    "type": "message",
                    "label": "詳細介紹",
                    "text": movieNameCN
                }
                }
            ]
            }
        }        
    )
    nowTime_flex_message = FlexSendMessage(
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
                "text": "現在時間",
                "align": "center",
                "weight": "bold"
                },
                {
                "type": "text",
                "text": time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()+28800)),
                "align": "center"
                }
            ]
            }
        }
    )
    return(movieInfo_flex_message, nowTime_flex_message, area_flex_message, movietheater_flex_message, pagebox_flex_message)


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
                    "text": "Yahoo電影、開眼電影網",
                    "align": "start",
                    "wrap": True
                    }
                ]
                }
            ]
            }
        }
    )
    return(workTeam_flex_message)
