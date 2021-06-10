import logging
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import BusPair
from .serializers import BusPairSerializer

logger = logging.getLogger(__name__)

class BusPairListCreateAPIView(generics.ListCreateAPIView):
    """バス組み合わせモデルの取得（一覧）・登録APIクラス"""
    queryset = BusPair.objects.all()
    serializer_class = BusPairSerializer


class BusPairRetrieveUpdateDestroyAPIView(
        generics.RetrieveUpdateDestroyAPIView):
    """バス組み合わせモデルの取得（詳細）・更新・一部更新・削除APIクラス"""
    queryset = BusPair.objects.all()
    serializer_class = BusPairSerializer
