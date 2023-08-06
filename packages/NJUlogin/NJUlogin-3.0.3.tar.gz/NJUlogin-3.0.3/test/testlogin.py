import json, time
from NJUlogin.pwdLogin import pwdLogin

dest = 'http://p.nju.edu.cn/cas/&renew=true'
mobile_headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; M2007J1SC Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/104.0.5112.97 Mobile Safari/537.36 cpdaily/9.0.15 wisedu/9.0.15'
}
pwdlogin = pwdLogin('191180118', 'TRis2002')
session = pwdlogin.login(dest)
assert session is not None, '登录失败'

url = 'http://p.nju.edu.cn/api/portal/v1/getinfo?_=%d' % int(time.time() * 1000)
res = pwdlogin.get(url, timeout=5)
# or:
# res = session.get(url, timeout=5)
data = json.loads(res.text)
print('余额: %.2f元' % (data['results']['rows'][0]['balance'] / 100))
pwdlogin.logout_all()
pwdlogin.logout()
