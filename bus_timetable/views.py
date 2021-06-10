import logging
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import BusTimetable
from .serializers import BusTimetableSerializer

logger = logging.getLogger(__name__)


class BusTimetableListCreateAPIView(generics.ListCreateAPIView):
    """バス時刻モデルの取得（一覧）・登録APIクラス"""
    queryset = BusTimetable.objects.all()
    serializer_class = BusTimetableSerializer


class BusTimetableRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView):
    """バス時刻モデルの取得（詳細）・更新・一部更新・削除APIクラス"""
    queryset = BusTimetable.objects.all()
    serializer_class = BusTimetableSerializer
