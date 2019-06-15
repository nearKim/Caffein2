import json
import os
import urllib.request

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@login_required
@csrf_exempt
def search_place(request):
    if request.method == "GET":
        # AJAX 리퀘스트에서 data에 search_term이 담겨 넘어온다.
        place = request.GET.get('search_term', '')
        # 초기화면 또는 빈칸 검색시
        if place == '':
            return render(request, 'cafes/place_search.html', context={'places': ''})

        encText = urllib.parse.quote(place)
        url = "https://openapi.naver.com/v1/search/local?display=10&query=" + encText  # json 결과

        request_obj = urllib.request.Request(url)
        request_obj.add_header("X-Naver-Client-Id", settings.LEGACY_NAVER_CLIENT_ID)
        request_obj.add_header("X-Naver-Client-Secret", settings.LEGACY_NAVER_CLIENT_SECRET)
        response = urllib.request.urlopen(request_obj)

        # 정상 작동시
        if response.getcode() == 200:
            response_body = response.read()
            search_results = json.loads(response_body.decode('utf-8'))
            places = search_results.pop('items')
            return render(request, 'cafes/place_search.html', context={'places': places})
        # 에러 발생시
        else:
            return render(request, 'cafes/place_search.html', context={'places': ''})
    else:
        # 네이버 API는 오직 GET요청만을 허용한다
        raise Http404
