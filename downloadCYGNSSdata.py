# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 18:32:52 2018

@author: shibukawa
"""
import requests
import urllib.request
from bs4 import BeautifulSoup
import os
import subprocess
import time
from datetime import datetime
import numpy as np

username = '********'
password = '**************'
aria_dir = r"C:\aria2\aria2c"
save_dir = r"C:\aria2\test"
dl_log = 'C:/aria2/datalist.txt'
file_dld = os.listdir(save_dir)

#コマンドプロンプト経由でaria2dを起動、1ファイルのみをURL指定してダウンロード、所要時間を返す
def dl_aria_cygnss(aria_dir,save_dir,username,password,connections,dl_url):
    save_cmd = r"--dir=" + save_dir
    user_cmd = r"--http-user=" + username
    pass_cmd = r"--http-passwd=" + password
    connection_cmd = r"-x" + str(connections)
    cmd = (aria_dir,save_cmd,user_cmd,pass_cmd,connection_cmd,dl_url) #コマンドプロンプトに打つコマンド
    start = time.time()
    result = subprocess.run(cmd,shell=True)
    elapsed_time = time.time() - start
    return elapsed_time
    
#    print(result)

#CYGNSSサーバの特定のファイルに入っている.ncファイル一覧を返す
def extractcygnssdata(url):
    page = requests.get(url, auth=(username, password)).text
    soup = BeautifulSoup(page, "html.parser")
    a = soup.find_all("tr",{"class":"odd"})
    b = []
    for x in a:
        b.append(str(x))
    result = []
    for x in b:
        a = (BeautifulSoup(x, "html.parser")).a.get("href")
        result.append(a)
    return result

#ファイル番号リスト内の全.ncファイルを1つずつダウンロードする
def dl_once_a_time(file_num_list):
    for file_num in file_num_list:
        file_num_str = str(file_num).zfill(3)
        url = r'https://podaac-uat.jpl.nasa.gov/drive/files/allData/cygnss/L1/v2.0/2018/' + file_num_str + '/'
        datalist = extractcygnssdata(url) #URL下のファイルリスト
        for data in datalist:
            f = open(dl_log,'a')
            if data in file_dld: #既にダウンロードされているものはスルー
                datenow = datetime.now().strftime("%Y/%m/%d %H:%M:%S") #現在時刻
                already_message = datenow + ' ' + data + ' Already Downloaded'
                f.write(already_message + '\n') #ログ書き込み
                print(already_message)
            else:
                dir_data = url + data
                elapsed_time = dl_aria_cygnss(aria_dir,save_dir,username,password,8,dir_data)
                datenow = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                datenow = datetime.now().strftime("%Y/%m/%d %H:%M:%S") #現在時刻
                complete_message = datenow + ' ' + dir_data + ' Done ' + "elapsed_time:{0}".format(elapsed_time) + "[sec]"
                f.write(complete_message + '\n') #ログ書き込み
                print(complete_message)
            f.close()

if __name__ == '__main__':
    #end:366
    file_num_list = np.arange(1,120)
    file_num_list = file_num_list.tolist()
    dl_once_a_time(file_num_list)