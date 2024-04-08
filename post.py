# 体温填报器
import re
import time

import execjs
import requests

import des


class Reporter:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        # self.temperature = 36.5
        # self.isOut = 2
        # self.address = ""
        # self.travelMode = ""
        self.nowTime = int(time.time() * 1000)
        self.session = requests.session()

    def get_cookies(self) -> None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/86.0.4240.198 Safari/537.36 "
        }
        pattern = re.compile(r'LT-.+-tpass')
        r = self.session.get("http://sso.ujn.edu.cn/tpass/login",
                             headers=headers)
        cookies = r.cookies
        lt = str(re.search(pattern, r.text).group(0))
        js = des.des_js_code
        compile_js = execjs.compile(js)
        rsa = compile_js.call("strEnc", self.username + self.password + lt, '1', '2', '3')

        params = {
            "rsa": str(rsa),
            "ul": str(len(self.username)),
            "pl": str(len(self.password)),
            "lt": lt,
            "execution": 'e1s1',
            "_eventId": 'submit',
        }
        self.session.post("http://sso.ujn.edu.cn/tpass/login",
                          params=params, allow_redirects=True, headers=headers, cookies=cookies)
        print(rsa)
        print(r.text)
    def post(self) -> str:
        data = {
            'xnm': '2022',
            'xqm': '3',
            '_search': 'false',
            'nd': f'{int(time.time() * 1000)}',
            'queryModel.showCount': '15',
            'queryModel.currentPage': '1',
            'queryModel.sortName': '',
            'queryModel.sortOrder': 'asc',
            'time': '1',
        }
        params = {
            'doType': 'query',
            'gnmkdm': 'gnmkdm',
            'su': 'su',
        }
        # cookies = {
        #     'JSESSIONID': '3C191E77ABBC898698DF85EC5BBCE4F8',
        # }

        r = self.session.post('http://jwgl.ujn.edu.cn/jwglxt/cjcx/cjcx_cxXsgrcj.html',
        params=params,
        # cookies=cookies,
        data=data,
        verify=False,)

        print(r)
        print(r.text)
        return r.text

post=Reporter('sid','pwd')
post.get_cookies()