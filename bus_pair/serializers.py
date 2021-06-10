from typing import Any, Dict
from django.db.models import fields
from rest_framework import serializers
from .models import BusPair
from busstop.models import Busstop
from busstop.serializers import BusstopSerializer

# DRFでシリアライザのForeignKeyフィールドをPOST時はプライマリーキーを渡し、GET時は展開する
# https://kimuson.dev/blog/django/drf_foreign_key_serializer/


class BusPairSerializer(serializers.ModelSerializer):
    """バス組み合わせモデル用のシリアライザ"""
    departure_bus_stop = BusstopSerializer(read_only=True)
    arrival_bus_stop = BusstopSerializer(read_only=True)

    departure_bus_stop_id = serializers.PrimaryKeyRelatedField(
        queryset=Busstop.objects.all(),
        write_only=True
    )
    arrival_bus_stop_id = serializers.PrimaryKeyRelatedField(
        queryset=Busstop.objects.all(),
        write_only=True
    )

    class Meta:
        model = BusPair
        fields = [
            'id',
            'departure_bus_stop',
            'arrival_bus_stop',
            'departure_bus_stop_id',
            'arrival_bus_stop_id']

    def create(self, validated_data: Dict[str, Any]) -> BusPair:
        validated_data['departure_bus_stop'] = validated_data.get(
            'departure_bus_stop_id', None)
        validated_data['arrival_bus_stop'] = validated_data.get(
            'arrival_bus_stop_id', None)

        if validated_data['departure_bus_stop'] is None:
            raise serializers.ValidationError("departure_bus_stop not found.")
        if validated_data['arrival_bus_stop'] is None:
            raise serializers.ValidationError("arrival_bus_stop not found.")

        del validated_data['departure_bus_stop_id']
        del validated_data['arrival_bus_stop_id']

        return super().create(validated_data)


class BusPairListSerializer(serializers.ListSerializer):
    """複数のバス組み合わせモデルを扱うためのシリアライザ"""
    child = BusPairSerializer()
