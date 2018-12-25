import pymysql
import requests as re
import time

def get_token():
    db = pymysql.connect('localhost','root','root','ERP')
    appid='wxec4567a41338530d'
    secret = 'f81a45edfb0ebb4607c8441fac0876d9'
    ass_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid, secret)
    raw = re.get(ass_url)
    raw.encoding = 'utf-8'
    token = raw.json()['access_token']
    expires = raw.json()['expires_in']
    cur = db.cursor()
    sql = "INSERT INTO account_access_token VALUES(%s,%s)" %(token,expires)
    try:
        cur.execute(sql)
        db.commit()
        print("获取token成功，token为%s" % token)
    except:
        db.rollback()
    db.close()


if __name__ == '__main__':
    while True:
        get_token()
        time.sleep(7200)
