import urllib.request
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# FIXME : 실제 활용 시에는 secret 파일로 숨김
client_id = "R8CudDUPo54uScENakHk"
client_secret = "1uo8grDpdo"


@login_required
@csrf_exempt
def search_place(request):
    if request.method == "POST":
        place = request.POST.get('search', '')
        # 빈칸 검색시
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
        # 정상 작동시
        if rescode == 200:
            response_body = response.read()
            items = json.loads(response_body.decode('utf-8'))
            return render(None, 'cafe/cafe_search.html', context=items)
        # 에러 발생시
        else:
            return render(None, 'cafe/cafe_search.html', context={'items': ''})
    else:
        return render(None, 'cafe/cafe_search.html', context={'items': ''})

