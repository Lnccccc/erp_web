import pymysql
import requests as re
import time


def get_token():
    i = 1

    db = pymysql.connect('localhost','root','root','ERP')
    appid='wxec4567a41338530d'
    secret = 'f81a45edfb0ebb4607c8441fac0876d9'
    ass_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid,secret)
    raw = re.get(ass_url)
    raw.encoding = 'utf-8'
    token = raw.json()['access_token']
    expires = raw.json()['expires_in']
    print('请求成功，token为%s' % token)
    cur = db.cursor()
    sql1 = "delete from account_access_token"
    sql2 = "INSERT into account_access_token (id,token,expires) VALUES (%d,'%s',%d)" %(i,token,expires)
    try:
        cur.execute(sql1)
        cur.execute(sql2)
        db.commit()
        print("插入token成功，token为%s" % token)
    except:
        print('error raise')
        db.rollback()
    db.close()



if __name__ == '__main__':
    while True:
        print('开始执行...')
        get_token()
        time.sleep(7200)
