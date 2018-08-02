import urllib.request
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt

client_id = "R8CudDUPo54uScENakHk"
client_secret = "1uo8grDpdo"

@csrf_exempt
def search_place(request):
    if request.method == "POST":
        place = request.POST.get('search','')
        if place == '':
            return render(None, 'cafe/cafe_search.html', context={'items': ''})
        encText = urllib.parse.quote(place)
        url = "https://openapi.naver.com/v1/search/local?display=20&query=" + encText # json 결과
        #url = "https://openapi.naver.com/v1/search/local.xml?sort=comment&display=20&query=" + encText # xml 결과
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            #print((response_body.decode('utf-8').split('\n')[6:-3]))
            #items = [s for s in (response_body.decode('utf-8').splitlines())][6:-2]
            items = json.loads(response_body.decode('utf-8'))
            print(items)
            return render(None, 'cafe/cafe_search.html', context=items)
        else:
            print("Error Code:" + rescode)
            return render(None, 'cafe/cafe_search.html', context={'items': ''})
    else:
        return render(None, 'cafe/cafe_search.html', context={'items': ''})

