#!/usr/bin/env python
# coding: utf-8

import requests
from requests.exceptions import ConnectionError
from pyquery import PyQuery as pq

from bs4 import BeautifulSoup

import json

import emoji
import re

import pandas as pd

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

# sentiment classification
semantic_cls = pipeline(Tasks.text_classification, 'damo/nlp_structbert_sentiment-classification_chinese-base')

def get_podcast_info(PID):
    # pid is the identifier of podcast host

    # get raw data
    url = "https://www.xiaoyuzhoufm.com/podcast/{}".format(PID)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'
    }
    # 需要更换自己的cookie
    cookies = {

    }

    req = requests.get(url,cookies=cookies, headers=headers, timeout=30)

    html=req.content
    raw_data=str(html,'utf-8')
    print(raw_data)
    with open('output1.html', 'w', encoding='utf-8') as file: 
        
        # 写入内容
        print(raw_data, file=file)

    json_pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'

    json_match = re.search(json_pattern, raw_data, re.DOTALL)

    if json_match:
        json_data = json_match.group(1)
        data = json.loads(json_data)
        print(data)

    # 创建BeautifulSoup对象
    soup = BeautifulSoup(raw_data, 'html.parser')

    # 使用find方法查找第一个匹配的<ul>标签
    podname = soup.find('title', class_="jsx-7bbe0f84186f1998")

    # 检查是否找到了标签并打印结果
    if podname:
        print(podname)
    else:
        print("没有找到匹配的<ul>标签")

    finalpodname = str(podname)[36:-24].replace(" ", "").replace("|","")
    # print(finalpodname)



    # 从某个开始没解析好（钱倩）
    # get eid_index in raw_data
    eid_index = [i for i in range(len(raw_data)) if raw_data.startswith('"type":"EPISODE","eid"', i)]

    # create list to store eid, eid is the identifier of each episode
    eid_list = []

    # get eid
    for val in eid_index:
        eid_list.append(raw_data[val+24:val+48])
    
    if not eid_list:
        return 0
        
    eid_names = {'id','level','likeCount','isFriendly','replyCount'}
    epi_info_data = [] # store basic info of every comments of episode 
    for val in eid_list:
        # get url of episode
        print(val)
        each_episode_url = "https://www.xiaoyuzhoufm.com/_next/data/quPA7j3prDFxOv8729MWU/episode/{}.json".format(val)

        fh = requests.get(each_episode_url,cookies=cookies, headers=headers)
        print(fh)
        json_data = fh.json()
        # print(json_data)
        
        # 使用json.dumps方法将字典转换成格式化的JSON字符串
        formatted_json = json.dumps(json_data['pageProps']['comments'], indent=4, sort_keys=True)

        # # 打印格式化的JSON字符串
        print(type(formatted_json))

        # get episode name
        episode_name = json_data['pageProps']['episode']['title']

        for i in json_data['pageProps']['comments']:
            epi_comment = {key: value for key, value in i.items() if key in eid_names}
            epi_comment['text'] = emoji.demojize(str(i['text']))
            epi_comment['epi_name'] = episode_name
            epi_comment['pod_name'] = finalpodname
            epi_comment['Sentiment'] = semantic_cls(input=i['text'])['scores'][0] # get the prob of positive
            print(epi_comment)

            epi_info_data.append(epi_comment)

    # convert to csv file
    import csv 

    # convert epi_info_data to csv
    info = ['pod_name','epi_name','id','level','text','isFriendly','Sentiment','likeCount','replyCount']
    with open(finalpodname + '_comments_data.csv', 'w' ,encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = info)
        writer.writeheader()
        writer.writerows(epi_info_data)

if __name__ == "__main__":

    # 读取Excel文件
    file_path = '2023大赏.xlsx'  # Excel文件路径
    sheet_name = 'All'  # Sheet名称

    # 使用pandas读取指定Sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 获取第二列的数据，假设列的索引从0开始计数
    # 如果列有标题，可以使用列标题直接访问
    second_column = df.iloc[:, 1]  # 第二列的索引为1

    # 打印第二列的数据
    for i in second_column:
        content_after_podcast = i.split("/podcast/")[-1]

        print(content_after_podcast)
        get_podcast_info(content_after_podcast)
