import logging
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import generics
from .models import Busstop
from .serializers import BusstopSerializer

logger = logging.getLogger(__name__)

class BusstopCreateAPIView(generics.CreateAPIView):
    """バス停モデルの登録APIクラス"""
    serializer_class = BusstopSerializer

    def create(self, request, *args, **kwargs):
        """バス停モデルの登録APIに対応するアクションメソッド"""
        response = super().create(request, *args, **kwargs)
        logger.info("Busstop(id={})を登録しました".format(response.data['id']))
        return response

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
