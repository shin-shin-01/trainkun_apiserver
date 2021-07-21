"""trainkun_apiserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import busstop.views as busstop_views
import bus_line.views as bus_line_views
import bus_pair.views as bus_pair_views
import bus_timetable.views as bus_timetable_views
import bus_timetable_bulk.views as bus_timetable_bulk_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # バス停モデルの取得（一覧）・登録
    path('api/busstops/', busstop_views.BusstopListCreateAPIView.as_view()),
    # バス停モデルの取得（詳細）・更新・一部更新・削除
    path(
        'api/busstops/<pk>/',
        busstop_views.BusstopRetrieveUpdateDestroyAPIView.as_view()),
    # バス路線モデルの取得（一覧）・登録
    path('api/bus_lines/', bus_line_views.BusLineListCreateAPIView.as_view()),
    # バス路線モデルの取得（詳細）・更新・一部更新・削除
    path(
        'api/bus_lines/<pk>/',
        bus_line_views.BusLineRetrieveUpdateDestroyAPIView.as_view()),
    # バス組み合わせモデルの取得（一覧）・登録
    path('api/bus_pairs/', bus_pair_views.BusPairListCreateAPIView.as_view()),
    # バス組み合わせモデルの取得（詳細）・更新・一部更新・削除
    path(
        'api/bus_pairs/<pk>/',
        bus_pair_views.BusPairRetrieveUpdateDestroyAPIView.as_view()),
    # バス時刻モデルの取得（一覧）・登録
    path(
        'api/bus_timetables/',
        bus_timetable_views.BusTimetableListCreateAPIView.as_view()),
    # バス時刻モデルの取得（詳細）・更新・一部更新・削除
    path(
        'api/bus_timetables/<pk>/',
        bus_timetable_views.BusTimetableRetrieveUpdateDestroyAPIView.as_view()),
    # バス時刻モデル一括登録
    path('api/bus_timetable_bulk/',
         bus_timetable_bulk_views.BusTimetableBulkCreateAPIView.as_view())
]
