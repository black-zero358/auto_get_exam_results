import re
import time
import execjs
import requests
import src.plugins.exam_score.des

def get(username, password):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/86.0.4240.198 Safari/537.36 "
    }

    sessions = requests.session()

    pattern = re.compile(r'LT-.+-tpass')
    r = sessions.get("http://sso.ujn.edu.cn/tpass/login?service=http%3A%2F%2Fjwgl.ujn.edu.cn%2Fsso%2Fdriotlogin",
                    headers=headers)

    print(sessions.cookies)
    cookies = r.cookies
    lt = str(re.search(pattern, r.text).group(0))
    js = des.des_js_code
    compile_js = execjs.compile(js)
    rsa = compile_js.call("strEnc", username + password + lt, '1', '2', '3')

    params = {
        "rsa": str(rsa),
        "ul": str(len(username)),
        "pl": str(len(password)),
        "lt": lt,
        "execution": 'e1s1',
        "_eventId": 'submit',
    }
    sessions.post("http://sso.ujn.edu.cn/tpass/login?service=http%3A%2F%2Fjwgl.ujn.edu.cn%2Fsso%2Fdriotlogin",
                 params=params, allow_redirects=True, headers=headers, cookies=cookies)

    params = {
        'doType': 'doType',
        'gnmkdm': 'gnmkdm',
        'su': 'sid',
    }

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

    response = sessions.post(
        'http://jwgl.ujn.edu.cn/jwglxt/cjcx/cjcx_cxXsgrcj.html',
        params=params,
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False,
    )
    print(response)

    cj = ''

    if ('{"' == response.text[0:2]):
        for i in response.json()['items']:
            if (any(name in i['kcmc'] for name in ['常微分', 'C', '离散', '分析', '数据', '英语'])):
                cj = cj + i['kcmc'] + " 成绩:" + i['cj'] + '\n'
    return (cj)
print(get('sid', 'pwd'))