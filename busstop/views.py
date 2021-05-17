from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import Busstop
from .serializers import BusstopSerializer

class BusstopCreateAPIView(generics.CreateAPIView):
    """バス停モデルの登録APIクラス"""
    serializer_class = BusstopSerializer

class BusstopListAPIView(generics.ListAPIView):
    """バス停モデルの取得（一覧）APIクラス"""
    queryset = Busstop.objects.all()
    serializer_class = BusstopSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = '__all__'

class BusstopRetrieveAPIView(generics.RetrieveAPIView):
    """バス停モデルの取得（詳細）APIクラス"""
    queryset = Busstop.objects.all()
    serializer_class = BusstopSerializer

class BusstopUpdateAPIView(generics.UpdateAPIView):
    """バス停モデルの更新・一部更新APIクラス"""
    queryset = Busstop.objects.all()
    serializer_class = BusstopSerializer

class BusstopDestroyAPIView(generics.DestroyAPIView):
    """バス停モデルの削除APIクラス"""
    queryset = Busstop.objects.all()
