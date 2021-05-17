import logging
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import Busstop
from .serializers import BusstopSerializer

logger = logging.getLogger(__name__)

class BusstopListCreateAPIView(generics.ListCreateAPIView):
    """バス停モデルの取得（一覧）・登録APIクラス"""
    queryset = Busstop.objects.all()
    serializer_class = BusstopSerializer

class BusstopRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """バス停モデルの取得（詳細）・更新・一部更新・削除APIクラス"""
    queryset = Busstop.objects.all()
    serializer_class = BusstopSerializer
