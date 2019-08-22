
# coding: utf-8

# In[1]:


import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver

import re
import itertools
import numpy as np


# In[2]:


def get_request_url(url, enc='euc_kr'):
    
    req = urllib.request.Request(url)
    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')    
            
            return ret
            
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None


# In[1]:


def getweatherAddress(stn,start_year,end_year,result,key):   
  
    obs = ["8","10","7","59","21","12","6"]
    obs_name = ["최고기온","최저기온","평균기온""평균운량","일강수량","상대습도","평균평속"]
    weekday = ["월","화", "수", "목", "금", "토", "일"]
    
    weather_URL = "http://www.weather.go.kr/weather/climate/past_table.jsp?"
    location = "stn=" + stn + "&"
    
    month = []
    day = []
    date = []
    week = []
    checkday = []
    tmp = []
    tt = []
    for y in range(int(start_year),int(end_year)):
        for i in range(1,13):
            tt.append(str(y) + "/" + str(i))
    
    result.append(tt)
    
    for observe in obs:
        for y in range(int(start_year),int(end_year)):
            
            year = "yy=" + str(y) + "&" 
            
            try:
                target_URL = weather_URL + location + year + "obs=" + str(observe)
                print(target_URL)

                rcv_data = get_request_url(target_URL)
                soupData = BeautifulSoup(rcv_data, 'html.parser')
                table_tag= soupData.find('table', attrs={'class': 'table_develop'})            

                for tr in table_tag.tbody.findAll("tr"):
                    date = []
                    a = tr.find("td", attrs={'scope': 'row'}).string
                    if str(a) == "평균" or str(a) =="합계":
                        for td in tr:
                                if td != "\n":
                                    if str(td.string) == "\xa0":
                                        date.append(0.001)
                                    elif str(td.string) == "평균" or str(td.string) =="합계":
                                        continue
                                    else:
                                        date.append(str(td.string))
                        day.append(date)
    
                a = np.array(day)
                a = np.transpose(a)
                a = a.reshape(-1)
                a = a.tolist()
                tmp.append(a)
                
                day = []
            except Exception as e:
                print(e)
                break
        a = np.array(tmp)
        a = a.reshape(-1)
        a = a.tolist()
#        print(a)
        result.append(a)
        tmp=[]
    
    end = []
    tmp = []
    #print(result)
    for i in range(0,len(result[0])):
        for j in range(0,len(result)):
            tmp.append(result[j][i])
        end.append(tmp)
        tmp = []
    #print(end)
    weather_table = pd.DataFrame(end, columns=("년월","최고기온","최저기온","평균기온","평균운량","일강수량","상대습도","평균평속"))
    weather_table.to_csv("./data/평균_%s_%s_%s.csv" % (start_year,int(end_year)-1,key), encoding="cp949", mode='w', index=True)
    return


# In[4]:


def main():
    #경기 --> 수원  강원 --> 춘천 충북 --> 충주 충남 --> 천안 전북 -->전주
    #전남 --> 여수 경북 --> 포항 경남 --> 창원
    #
    stn = {"서울(유)" : "108","부산(유)" : "159",
           "대구(유)" : "143","인천(유)": "112" ,
           "광주(유)" : "156","대전(유)" : "133",
           "울산(유)" : "152","제주(유)" : "184",
           "경기(유)" : "119"," 강원(무)" : "101",
           "충북(유)" : "131", "충남(무)" : "232",
           "전북(유)" : "146", "전남(유)" : "168",
           "경북(유)" : "138", "경남(유)" : "155"
          }
    #stn = {"서울(유)" : "108" ,"백령도(유)" : "102" , "동두천(무)" : "98" , "파주(무)":"99"  , 
    #   "인천(유)": "112" , "수원(유)": "119", "강화(무)": "201" , "양평(무)":  "202" ,"이천(무)" : "203", 
    #   "북춘천(유)" : "93" , "철원(무) " : "95", "춘천(무)" :  "101", "원주(무)" :  "114" , "영월(무)" : "121",
    #   "인제(무)" : "211", "홍천(무)" : "212", "북강릉(유)" : "104", "울릉도(유)" : "115", "강릉(무)" : "105", "속초(무)" : "90",
    #   "대관령(무) " : "100", "동해(무)" : "106", "태백(무)" : "216", "정선군(무)" : "217", "청주(유)" : "131" , "충주(무)" : "127",
    #   "추풍령(무)" : "135", "제천(무)" : "221", "보은(무)" : "226" , "홍성(유)" : "177", "대전(유)" : "133", 
    #   "서산(무)" : "129", "천안(무)" : "232" , "보령(무)" : "235", "부여(무) " : "236","금산(무)" : "238",
    #   "전주(유)" : "146", "군산(무)" : "140" , "부안(무)" : "243", "임실(무) " : "244" , "정읍(무)" : "245","남원(무)" : "247",
    #   "장수(무)" : "248", "순창(무)" : "254","고창(무)" : "172", "고창(구)" : "251", "광주(유)" : "156", "목포(유)" : "165", 
    #   "흑산도(유)" : "169", "여수(유)" : "168", "완도(무)" : "170", "진도(첨찰산)(무)" : "175" , "진도군(무)" : "268",
    #   "영광(무)" : "252", "순천(무)" : "174", "순천(구)" : "256", "장흥(무)" : "260", "해남(무)" : "261", "고흥(무)" : "262",
    #   "강진군(무)" : "259", "보성군(무)" : "258", "광양(무)" : "266", "안동(유)" : "136", "포항(유)" : "138", "대구(유)" : "143",
    #   "대구(구)" : "176", "울진(무)" : "130", "상주(무)" : "137", "봉화(무)" : "271", "영주(무)" : "272", "문경(무)" : "273",
    #   "영덕(무)" : "277", "의성(무)" : "278", "구미(무)" : "279", "영천(무)" : "281", "청송군(무)" : "276","경주(무)" : "283",
    #   "부산(유)" : "159", "울산(유)" : "152", "창원(유)" : "155", "북창원(무)" : "255", "통영(무)" : "162", "진주(무)" : "192", 
    #   "거창(무)" : "284", "합천(무)" : "285", "밀양(무)" : "288", "산청(무)" : "289", "거제(무)" : "294", "남해(무)" : "295",
    #   "김해시(무)" : "253" , "양산(무)" : "257", "의령군(무)" : "263", "함양군(무)" : "264", "제주(유)" : "184", "고산(무)" : "185", 
    #   "서귀포(무)" : "189", "성산(무)" : "188"}
    result = []
    
    for key, value in stn.items():
        getweatherAddress(str(value),"1990","2017",result,key)
        
        result = []

    print('FINISHED')


# In[5]:


if __name__ == '__main__':
     main()

