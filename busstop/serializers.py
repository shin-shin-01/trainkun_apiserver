from django.db.models import fields
from rest_framework import serializers
from .models import Busstop

class BusstopSerializer(serializers.ModelSerializer):
    """バス停モデル用のシリアライザ"""
    class Meta:
        model = Busstop
        fields = ['id', 'name', 'code']

class BusstopListSerializer(serializers.ListSerializer):
    """複数のバス停モデルを扱うためのシリアライザ"""
    child = BusstopSerializer()