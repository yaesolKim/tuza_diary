# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

# websocket api
import websockets
import asyncio

from .models import Post, Market
from datetime import datetime

from .library.graphs import draw_candle_with_indicator
from .library.trading_indicators import bollinger_band, data_settings

from plotly.offline import plot


@login_required(login_url="/login/")
def index(request):
    # 처음 접속하면 무조건 로그인 페이지인가보다.
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


# 해당 종목의 데이터를 가져와서 보여주기
def get_data(code):
    # 종목별 데이터 언제부터 가져올지 설정
    coin_df = data_settings(code=code, start=datetime(2018, 1, 1))
    fig = draw_candle_with_indicator(coin_df, code)
    plt_div = plot(fig, output_type='div')
    return plt_div


# post.html 페이지를 부르는 post 함수
def post(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    plt_div = get_data(post.code)
    # post.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'main/post.html', {'post': post, 'plt_div': plt_div})


def market(request):
    # markets = Market.object.all()
    # context = {'markets': markets}
    context = {}
    html_template = loader.get_template('market.html')

    return HttpResponse(html_template.render(context, request))
    # return render(request, 'market.html', context)


def recon_chart(request, pk):
    coin_df = data_settings(code='005930', start=datetime(2018, 1, 1))
    fig = draw_candle_with_indicator(coin_df, '005930')
    plt_div = plot(fig, output_type='div')
    # post.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'recon_chart.html', {'post': post, 'plt_div': plt_div})


async def get_coin_data_by_websocket():
    uri = "wss://pubwss.bithumb.com/pub/ws"

    async with websockets.connect(uri, ping_interval=None) as websocket:
        greeting = await websocket.recv()
        print(greeting)

        # 구독 요청
        data = '{"type":"ticker", "symbols": ["BTC_KRW"], "tickTypes": ["30M"]}'
        await websocket.send(data)

        print("after send data")

        while True:
            recv_data = await websocket.recv()
            print(recv_data)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(get_coin_data_by_websocket())
