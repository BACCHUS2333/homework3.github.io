import requests
import re  # 正则表达式库，比如https://codegeex.cn 。任务是找出所有以下
import pandas as pd
import numpy as np  # 数组处理库，比如https://codegeex.cn 。任务是找出所有
import time
import os


def login():
    url = 'https://www.zhihu.com/signin?next=%2F'
    headers = { 
        'Content-Type': "application/json" 
    } 
    payload = {
       "usercode": "13601376502",
       "password": "Bacchus69247"
    }    
    try:
        res = requests.post(url, headers=headers, json=payload)
        cookies = res.cookies
        cookie = requests.utils.dict_from_cookiejar(cookies)     
        return cookie
    except Exception as err:
        print('获取cookie失败：\n{0}'.format(err))
print(login())
cookie = login()


cookie = '_zap=e767d0e4-7332-4b12-940b-2b699149467c; d_c0=ANBXmexClBaPTgzAZw3WICnBVonIMDjKjUc=|1680686777; YD00517437729195:WM_TID=SAgpNIMWoQlABEAFRULBPycAi6M38jBz; __snaker__id=UAyfCvyTNl5r5a3Z; YD00517437729195:WM_NI=FgwXN/dVILtnkyp1OzRtFMJTLR8jQZDheXNggVXjjyCcNQ6IgOaQD9lUyoE4oYDKcLcDamlOYviN5/hNTtxd3Dq5nXGbn55ZdNnpyMjDdHsTq9hAKRNMzYC4rUSO//kKT08=; YD00517437729195:WM_NIKE=9ca17ae2e6ffcda170e2e6eeb1d34da2b683d5f8478fac8fa6c55e869a9f87d448f5eaf98caa3ceda6b7d0b32af0fea7c3b92a86b9b9b9cd25a88a87adf766a9a7c0d2ce7292ac8aaec960908ef88bd45288b8abb9cd6da58a988be97381bd82b2b543a591afb2c733b08bb790c840ad878cace248a19caf8eef459baaa7afb825ac929c95fb70f19cbfd6ed5485bea2d6b852a892a291fc47aa9caca9f260b3e7a8a2ca5a8e93b6bac240b28b9db0ae25a9959cd1bb37e2a3; _xsrf=c9f40a4b-4a7b-4c09-8cbb-756492ffdc69; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1683420552,1683543377,1683620784,1683682466; q_c1=26340a5617b14821bf63287cdc069d41|1683682890000|1683682890000; z_c0=2|1:0|10:1683683219|4:z_c0|92:Mi4xeGMzdkJBQUFBQUFBMEZlWjdFS1VGaVlBQUFCZ0FsVk5QRVJJWlFCT1hLSEU5SkhzYVpMeGNXN3BBcmZzYUZaVkZB|ac9ecaa1b46fc2febd47f619b3d42f2a87769f5f661bc35a0efa663f4b7250fe; SESSIONID=SRFsCQad3M6ybYdM7ETAypA2YNdhLyjnFU9rIoyRbdl; JOID=VV8RA0mpul5cVQM7da-fRRmpRqpg-uscLRNSWRWf92shNV9fO7pFAj9QADxzXn34nY5v9__AVlzRS7YWTJp3mtU=; osd=U18SBUmvul1aVQU7dqmfQxmqQKpm-ugaLRVSWhOf8WsiM19ZO7lDAjlQAzpzWH37m45p9_zGVlrRSLAWSpp0nNU=; gdxidpyhxdE=746k+XMGy0Vaoj2DWi/cJa1G2yXUnfcsL9g+fLoHU7j45lSphnSQ3OsEA+Wo8r+ad8W+n4BKGTfcilggdTh8hpcD7ZHBbDDhstxPJhVTfsQs5lViZqjZ7pUgTW/iyKjWsscdh96/u3jbCm6Ax20360nfmGOaLRCgo4m4rwZt2vt+LHX1:1683684316436; tst=h; KLBRSID=e42bab774ac0012482937540873c03cf|1683683696|1683682469; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1683683697'

def get_time(fmt:str='%Y-%m-%d %H-%M-%S') -> str:
    '''
    获取当前时间
    '''
    ts = time.time()
    ta = time.localtime(ts)
    t = time.strftime(fmt, ta)
    return t


def save_hot_list() -> None:
    # 请求头
    headers = {

        'User-Agent': 'osee2unifiedRelease/4318 osee2unifiedReleaseVersion/7.7.0 Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Host': 'api.zhihu.com',


    }
    # 请求参数
    params = (
        ('limit', '50'),
        ('reverse_order', '0'),
    )
    # 发送请求
    response = requests.get(
        'https://zhihu.com/topstory/hot-list', headers=headers, params=params)

    items = response.json()['data']
    rows = []
    now = get_time()
    # 取日期为文件夹名称
    dir_path = now.split(' ')[0]
    # 文件夹不存在则创建
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    # 遍历全部热榜，取出几个属性
    for rank, item in enumerate(items, start=1):
        target = item.get('target')
        title = target.get('title')
        answer_count = target.get('answer_count')
        hot = int(item.get('detail_text').split(' ')[0])
        follower_count = target.get('follower_count')
        question_url = target.get('url').replace(
            'api', 'www').replace('questions', 'question')
        rows.append({
            '排名': rank,
            '标题': title,
            '回答数': answer_count,
            '关注数': follower_count,
            '热度(万)': hot,
            '问题链接': question_url
        })
    df = pd.DataFrame(rows)
    now = get_time()
    csv_path = dir_path+'/'+now+'zhihu_hot.csv'
    
    df.to_csv(csv_path, encoding='utf-8-sig', index=None)
    print(df)
    print(now, '的热榜数据数据已保存到文件', csv_path)

# 保存热榜数据
save_hot_list()