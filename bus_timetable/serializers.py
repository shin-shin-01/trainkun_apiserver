from typing import Any, Dict
from django.db.models import fields
from rest_framework import serializers
from .models import BusTimetable
from bus_pair.models import BusPair
from bus_pair.serializers import BusPairSerializer
from bus_line.models import BusLine
from bus_line.serializers import BusLineSerializer


class BusTimetableSerializer(serializers.ModelSerializer):
    """バス時刻モデル用のシリアライザ"""
    bus_pair = BusPairSerializer(read_only=True)
    bus_line = BusLineSerializer(read_only=True)

    bus_pair_id = serializers.PrimaryKeyRelatedField(
        queryset=BusPair.objects.all(),
        write_only=True
    )
    bus_line_id = serializers.PrimaryKeyRelatedField(
        queryset=BusLine.objects.all(),
        write_only=True
    )

    class Meta:
        model = BusTimetable
        fields = [
            'id',
            'bus_pair',
            'bus_line',
            'bus_pair_id',
            'bus_line_id',
            'departure_at',
            'arrive_at',
        ]

    def create(self, validated_data: Dict[str, Any]) -> BusTimetable:
        validated_data['bus_pair'] = validated_data.get(
            'bus_pair_id', None)
        validated_data['bus_line'] = validated_data.get(
            'bus_line_id', None)

        if validated_data['bus_pair'] is None:
            raise serializers.ValidationError("bus_pair not found.")
        if validated_data['bus_line'] is None:
            raise serializers.ValidationError("bus_line not found.")

        del validated_data['bus_pair_id']
        del validated_data['bus_line_id']

        return super().create(validated_data)


class BusTimetableListSerializer(serializers.ListSerializer):
    """複数のバス時刻モデルを扱うためのシリアライザ"""
    child = BusTimetableSerializer()
