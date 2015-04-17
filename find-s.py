#!/usr/bin/env python
#coding=utf-8

instance = []
h = [None, None, None, None, None,None]
# 获得数据
def getX():
    with open('data.txt') as f:
        for line in f:
            instance.append(line.strip())

# 学习函数
def learn():
    for line in instance:
        sky, air, humidity, wind, water, forecast, enjoy = line.split()
        if enjoy == 'Yes':
            if h[0] == None:
                h[0] = sky
            else:
                if h[0] != sky and h[0] != '?':
                    h[0] = '?'
            if h[1] == None:
                h[1] = air
            else:
                if h[1] != air and h[1] != '?':
                    h[1] = '?'
            if h[2] == None:
                h[2] = humidity
            else:
                if h[2] != humidity and h[2] != '?':
                    h[2] = '?'
            if h[3] == None:
                h[3] = wind
            else:
                if h[3] != wind and h[3] != '?':
                    h[3] = '?'
            if h[4] == None:
                h[4] = water
            else:
                if h[4] != water and h[4] != '?':
                    h[4] = '?'
            if h[5] == None:
                h[5] = forecast
            else:
                if h[5] != forecast and h[5] != '?':
                    h[5] = '?'

# 预测函数
def predict():
    sky, air, humidity, wind, water, forecast = raw_input('Please input the status:').split()
    if (h[0] == '?' or sky == h[0]) and (h[1] == '?' or air == h[1]) and (h[2]=='?' or h[2] == humidity) and (h[3] == '?' or h[3] == wind) and (h[4]=='?' or h[4] == water) and (h[5] == '?' or h[5] == forecast):
        print 'h(%s,%s,%s,%s,%s,%s) = 1' %(sky,air,humidity, wind,water,forecast)
    else:
        print 'h(%s,%s,%s,%s,%s,%s) = 0' %(sky,air,humidity, wind,water,forecast)

if __name__ == "__main__":
    getX()
    learn()
    print 'h='+str(h)
    predict()
