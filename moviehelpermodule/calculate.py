from math import radians, atan, tan, acos, cos, sin
import time

def getDistance(latA, lonA, latB, lonB):  
    ra = 6378140  # radius of equator: meter  
    rb = 6356755  # radius of polar: meter  
    flatten = (ra - rb) / ra  # Partial rate of the earth  
    # change angle to radians  
    radLatA = radians(latA)  
    radLonA = radians(lonA)  
    radLatB = radians(latB)  
    radLonB = radians(lonB)  
    
    pA = atan(rb / ra * tan(radLatA))  
    pB = atan(rb / ra * tan(radLatB))  
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))  
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2  
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2  
    dr = flatten / 8 * (c1 - c2)  
    distance = ra * (x + dr)
    return round(distance/1000,2)

def getNowTimeEmoji():
    nowHour = int(time.strftime("%H", time.localtime(time.time()+28800)))
    nowMinute = int(time.strftime("%M", time.localtime(time.time()+28800)))

    if nowHour in [0, 12]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕛"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕧"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕐"
    elif nowHour in [1, 13]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕐"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕜"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕑"
    elif nowHour in [2, 14]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕑"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕝"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕒"
    elif nowHour in [3, 15]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕒"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕞"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕓"
    elif nowHour in [4, 16]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕓"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕟"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕔"
    elif nowHour in [5, 17]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕔"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕠"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕕"
    elif nowHour in [6, 18]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕕"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕡"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕖"
    elif nowHour in [7, 19]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕖"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕢"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕗"
    elif nowHour in [8, 20]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕗"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕣"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕘"
    elif nowHour in [9, 21]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕘"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕤"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕙"
    elif nowHour in [10, 22]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕙"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕥"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕚"
    elif nowHour in [11, 23]:
        if nowMinute >= 0 and nowMinute < 15 :
            nowTimeEmoji = "🕚"
        elif nowMinute >= 15 and nowMinute < 45 :
            nowTimeEmoji = "🕦"
        elif nowMinute >= 45 and nowMinute < 60 :
            nowTimeEmoji = "🕛"

    return(nowTimeEmoji)