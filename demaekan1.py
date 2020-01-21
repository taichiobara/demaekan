# -*- coding: utf-8 -*-

"""
北海道1
青森県2
岩手県3
宮城県4
秋田県5
山形県6
福島県7
茨城県8
栃木県9
群馬県10
埼玉県11
千葉県12
東京都13
神奈川県14
新潟県15
富山県16
石川県17
福井県18
山梨県19
長野県20
岐阜県21
静岡県22
愛知県23
三重県24
滋賀県25
京都府26
大阪府27
兵庫県28
奈良県29
和歌山県30
鳥取県31
島根県32
岡山県33
広島県34
山口県35
徳島県36
香川県37
愛媛県38
高知県39
福岡県40
佐賀県41
長崎県42
熊本県43
大分県44
宮崎県45
鹿児島県46
沖縄県47
"""


#このリストは多分あってるかとは思うんだけれど、まちがっていたらごめん
#https://demae-can.com/search/address/city/24000000000/?typeId=5&beBlockCode=&addressId=&chainId=&genreNm=youshoku
#県を選択する時の↑こんな感じのURLの〜〜000000000の〜〜の部分の数字をnumに入れてね。（01の時は1とうつ感じで）


# # 最初からやる場合

#必要な道具の準備
from tqdm import tqdm
# from urllib import request
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup
import csv
from urllib import request
import requests
import urllib.parse
import pandas as pd
import pickle

#欲しい県の番号をnumに代入（例：北海道のとき、num=1）
num=1
#↑ここ


if num<10:
    num1="0"+str(num)
else:
    num1=str(num)
    
#県ごとのURL
url="https://demae-can.com/search/address/city/"+str(num1)+"000000000/?typeId=5&beBlockCode=&addressId=&chainId=&genreNm=youshoku"
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent': user_agent}

request = urllib.request.Request(
    url=url,
    headers=headers
    )
try:
    response = urllib.request.urlopen(request)
    time.sleep(2)


    #url_list（市区町村リスト）をつくる
    url_list=[]
    soup=BeautifulSoup(response,'html.parser')
    a=soup.find('div',class_="p_card_02 pt_acd-wrap_01 pB07_pc pB04_sp")
    b=a.find_all('a')
    for i in b:
        try:
            url_dic={"prefecture":"","place":"","url":""}
            url_dic["prefecture"]=soup.find('div',class_="p_ttl-l_03 first").find('h1').text
            url_dic["place"]=i.text
            url_dic["url"]=i["href"]
            url_list.append(url_dic)    
        except:
            print("　上の市区町村についてurl_listをを作る際にエラーが発生しました。")
    print("url_listを作り終えました")
except:
    print('市区町村リストを作る際にエラーが発生しました。')


#place_list（地域リスト）をつくる
place_list=[]
for i in tqdm(url_list):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        request = urllib.request.Request(
            url=i['url'],
            headers=headers
            )

        response = urllib.request.urlopen(request)
        time.sleep(2)
        soup=BeautifulSoup(response,'html.parser')
        for i in soup.find_all('a',class_="select_address"):
            place_dic={"name":"","url":""}
            place_dic["name"]=i.text
            place_dic['url']=i["data-next_url"]
            place_list.append(place_dic)
    except:
        print('place_listを作る際にエラーが発生しました。')
        print(i['url'])

#place_list_name="place_list"+str(num)+".pickle"
# with open(place_list_name, 'wb') as f:
#     pickle.dump(place_list, f)
print("place_listを作り終えました") 
        

#place_list_2（最終的なリスト）をつくる。
place_list_2=[]
for place in tqdm(place_list):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        request = urllib.request.Request(
            url=place['url'],
            headers=headers
            )
        response = urllib.request.urlopen(request)
        time.sleep(2)
        soup=BeautifulSoup(response,'html.parser')
        try:
            AB=str(soup.find("div",class_="p_ttl-l_02").text)
        except:
            AB=""
        try:
            CD =soup.find('div',class_="shop-menu").text
        except:
            CD=""

        if "以下から地域を選択してください" in AB:
            for i in soup.find_all('a',class_="select_address"):
                place_dic_2={"name":"","url":""}
                place_dic_2["name"]=place['name']+i.text
                place_dic_2['url']=i["data-next_url"]
                place_list_2.append(place_dic_2)
        elif "条件に一致する店舗が存在しませんでした。" in CD:
            pass

        else:
            place_dic_2={"name":"","url":""}
            place_dic_2["name"]=place['name']
            place_dic_2['url']=place["url"]
            place_list_2.append(place_dic_2)
    except:
        print('以下のURLからplace_listを作る際にエラーが発生しました　。')
        print(place['url'])
        
place_list_2_name="place_list_2"+str(num)+".pickle"
with open(place_list_2_name, 'wb') as f:
    pickle.dump(place_list_2, f)
print(place_list_2_name+"を作り終えました")  

info_list=[]
for place in tqdm(place_list_2):
#for place in a:
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        request = urllib.request.Request(
            url=place["url"],
            headers=headers
            )
        response = urllib.request.urlopen(request)
        time.sleep(2)
        soup=BeautifulSoup(response,'html.parser')
        shops=soup.find_all("div",class_="shop_list-menu")
        for i in shops:
            info_dic={"place":"","name":"","url":"","image":"","price":"","postage":"","good_rate":"","review_num":"","time":""}
            info_dic["place"]=soup.find("div",class_="current_local target_address-inner changeAddressTrigger").find('span').text
            info_dic["name"]=i.find("div",class_="menu-info_02").text
            info_dic["url"]=i.find("a",class_="addAddrIdZip")["href"]
            try:
                info_dic["image"]="https://"+i.find("img",class_="lazy")["data-original"][6:]
            except:
                info_dic["image"]=""
            try:
                info_dic["price"]=i.find("div",class_="menu-info_03").find_all("div")[0].text
            except:
                info_dic["price"]=""
            try:
                info_dic["postage"]=i.find("div",class_="menu-info_03").find_all("div")[1].text
            except:
                 info_dic["postage"]=""
            try:
                info_dic["good_rate"]=i.find("div",class_="col01").find("span")["style"][6:][:-1]
            except:
                info_dic["good_rate"]=""
            try:
                info_dic["review_num"]=i.find("div",class_="col02").text[1:][:-1]
            except:
                info_dic["review_num"]=""
            try:
                info_dic["time"]=i.find("div",class_="took_time").text
            except:
                info_dic["time"]=""
            info_list.append(info_dic)
    except:
        print("エラーです"+place["url"])


#info_listができました。
# CSV化
data=pd.DataFrame(info_list)
#data=data.drop_duplicates(subset='item_code')
file_name="infolist"+str(num)+".csv"
data.to_csv(file_name,encoding='utf_8_sig')
print(str(num)+"についておわりました！")


