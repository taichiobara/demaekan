# # place_list_2（コレをつくるのに時間がかかる）まで作り終えたときに途中から再開するには

from tqdm import tqdm
from urllib import request
from bs4 import BeautifulSoup
import time
from bs4 import BeautifulSoup
import csv
from urllib import request
import requests
import urllib.parse
import pandas as pd
import pickle
import random

#欲しい県の番号をnumに代入（例：北海道のとき、num=1）
num=1
#↑ここ

#リストのpickleを読み出す
place_list_2_name="place_list_2"+str(num)+".pickle"
with open(place_list_2_name, 'rb') as f:
    place_list_2 = pickle.load(f)



info_list=[]
sum=0
print('-----------------------------------------------------------')
print("リストの長さは"+str(len(place_list_2))+"です")
print('-----------------------------------------------------------')
place_list_2_num=len(place_list_2)//10
print(place_list_2_num)

for place in tqdm(place_list_2):
    sum=sum+1
#for place in a:
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        headers = {'User-Agent': user_agent}

        request = urllib.request.Request(
            url=place["url"],
            headers=headers
            )
        response = urllib.request.urlopen(request)
        time.sleep(random.uniform(1.5,3))
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
    if sum%place_list_2_num==0:
        data=pd.DataFrame(info_list)
        file_name="infolist"+str(num)+"_"+str(sum)+".csv"
        data.to_csv(file_name,encoding='utf_8_sig')
        print(file_name+"を出力しました。")
        



#info_listができました。
# CSV化
data=pd.DataFrame(info_list)
#data=data.drop_duplicates(subset='item_code')
file_name="infolist"+str(num)+"_last"+".csv"
data.to_csv(file_name,encoding='utf_8_sig')
print(str(num)+"についておわりました！")
