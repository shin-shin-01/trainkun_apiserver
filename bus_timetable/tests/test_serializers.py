from django.test import TestCase
from django.utils.timezone import localtime
from rest_framework import serializers
from collections import OrderedDict

from ..models import BusPair
from ..serializers import BusPairSerializer
from busstop.factories import BusstopFactory
from busstop.serializers import BusstopSerializer


class TestBusPairSerializer(TestCase):
    """BusPairSerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK）"""
        departure_bus_stop = BusstopFactory()
        arrival_bus_stop = BusstopFactory()

        # シリアライザを作成
        input_data = {
            'departure_bus_stop_id': departure_bus_stop.id,
            'arrival_bus_stop_id': arrival_bus_stop.id,
        }
        serializer = BusPairSerializer(data=input_data)
        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    # 入力データのバリデーション（NG：name, codeが空文字）
    # db_constraint=False のため Error が発生しない

    def test_output_data(self):
        """出力データの内容検証"""
        departure_bus_stop = BusstopFactory()
        arrival_bus_stop = BusstopFactory()
        departure_bus_stop_serializer = BusstopSerializer(
            instance=departure_bus_stop)
        arrival_bus_stop_serializer = BusstopSerializer(
            instance=arrival_bus_stop)

        # シリアライザを作成
        bus_pair = BusPair.objects.create(
            departure_bus_stop=departure_bus_stop,
            arrival_bus_stop=arrival_bus_stop,
        )
        serializer = BusPairSerializer(instance=bus_pair)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': bus_pair.id, 'departure_bus_stop': OrderedDict(
                departure_bus_stop_serializer.data), 'arrival_bus_stop': OrderedDict(
                arrival_bus_stop_serializer.data), }

        self.assertDictEqual(serializer.data, expected_data)
