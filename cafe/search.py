import json
import urllib.request

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
            return render(request, 'cafe/cafe_search.html')
        encText = urllib.parse.quote(place)
        url = "https://openapi.naver.com/v1/search/local?display=20&query=" + encText  # json 결과

        request_obj = urllib.request.Request(url)
        request_obj.add_header("X-Naver-Client-Id", client_id)
        request_obj.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(request_obj)

        # 정상 작동시
        if response.getcode() == 200:
            response_body = response.read()
            search_results = json.loads(response_body.decode('utf-8'))
            places = search_results.pop('items')
            print(type(places))
            return render(request, 'cafe/cafe_search.html', context={'places': places})
        # 에러 발생시
        else:
            return render(request, 'cafe/cafe_search.html')
    else:
        return render(request, 'cafe/cafe_search.html')
