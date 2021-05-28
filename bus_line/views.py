import logging
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import BusLine
from .serializers import BusLineSerializer

logger = logging.getLogger(__name__)


class BusLineListCreateAPIView(generics.ListCreateAPIView):
    """バス路線モデルの取得（一覧）・登録APIクラス"""
    queryset = BusLine.objects.all()
    serializer_class = BusLineSerializer


class BusLineRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView):
    """バス路線モデルの取得（詳細）・更新・一部更新・削除APIクラス"""
    queryset = BusLine.objects.all()
    serializer_class = BusLineSerializer
