import requests 
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
