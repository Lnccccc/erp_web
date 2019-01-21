from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.shortcuts import render

def get_code(request):
    cd = request.GET.get('code')
    appid = 'wxf6d9517d8a850ecd'
    secret = '177546a750a8c8d12e45f94f39c18a61'
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (appid,secret,cd)
    if cd:
        return HttpResponse(cd)
    else:
        return redirect('/flow/')
    # req = re.get(url).json()
    # raw = json.loads(req)
    # ass_tok = raw['access_token']
    # open_id = raw['openid']
    # return HttpResponse(ass_tok)

def verifed(request):
    f=open("MP_verify_YUe1siIcc5wabsNm.txt",'rb')
    return  HttpResponse(f)

def homepage(request):
    return render(request,'index.html')
