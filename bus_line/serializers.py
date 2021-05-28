from django.db.models import fields
from rest_framework import serializers
from .models import BusLine


class BusLineSerializer(serializers.ModelSerializer):
    """バス路線モデル用のシリアライザ"""
    class Meta:
        model = BusLine
        fields = ['id', 'name', 'code']


class BusLineListSerializer(serializers.ListSerializer):
    """複数のバス路線モデルを扱うためのシリアライザ"""
    child = BusLineSerializer()
