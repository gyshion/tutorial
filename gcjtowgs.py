from math import pi,sqrt,sin,cos
import random
# Mars <==> WGS

# Krasovsky 1940
#
# a = 6378245.0, 1/f = 298.3
# b = a * (1 - f)
# ee = (a^2 - b^2) / a^2
a = 6378245.0
ee = 0.00669342162296594323

def wgstogcj(wgLat, wgLon):
    if (outOfChina(wgLat, wgLon)):
        mgLat = wgLat
        mgLon = wgLon
        return
    dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
    mgLat = wgLat + dLat
    mgLon = wgLon + dLon
    return mgLat,mgLon

def outOfChina(lat, lon):
    if (lon < 72.004 or lon > 137.8347):
        return True
    if (lat < 0.8293 or lat > 55.8271):
        return True
    return False

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret

# default accuracy: 0.00001, ~1m
def gcjtowgs(gcjLat, gcjLon ,accuracy = 0.00001, maxtry = 20):
    initDelta = 0.01
    dLat = initDelta
    dLon = initDelta
    mLat = gcjLat - dLat
    mLon = gcjLon - dLon
    pLat = gcjLat + dLat
    pLon = gcjLon + dLon
    while maxtry > 0:
        wgsLat = (mLat + pLat) / 2 + (random.random()-0.5)*0.1*accuracy
        wgsLon = (mLon + pLon) / 2 + (random.random()-0.5)*0.1*accuracy
        y,x = wgstogcj(wgsLat, wgsLon)
        dLat = y - gcjLat
        dLon = x - gcjLon
        if abs(dLat) < accuracy and abs(dLon) < accuracy:
            break
        maxtry -= 1
        if dLat > 0:
            pLat = wgsLat
        else:
            mLat = wgsLat
        if dLon > 0:
            pLon = wgsLon
        else:
            mLon = wgsLon
    return wgsLat,wgsLon


#WGS84_Lat = 39.990205
#WGS84_Long = 116.327847

#y,x = wgstogcj(WGS84_Lat,WGS84_Long)
#print y,x
#print gcjtowgs(y,x,0.00000000001)
 