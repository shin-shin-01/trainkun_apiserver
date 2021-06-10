import pytz
from django.test import TestCase
from django.utils.timezone import localtime
from rest_framework import serializers
from collections import OrderedDict
from factory.faker import faker

from ..models import BusTimetable
from ..serializers import BusTimetableSerializer
from bus_pair.factories import BusPairFactory
from bus_pair.serializers import BusPairSerializer
from bus_line.factories import BusLineFactory
from bus_line.serializers import BusLineSerializer

FAKE = faker.Faker()
jst = pytz.timezone('Asia/Tokyo')


class TestBusTimetableSerializer(TestCase):
    """BusTimetableSerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK）"""
        bus_pair = BusPairFactory()
        bus_line = BusLineFactory()
        departure_at = FAKE.date_time(tzinfo=jst)
        arrive_at = FAKE.date_time(tzinfo=jst)

        # シリアライザを作成
        input_data = {
            'bus_pair_id': bus_pair.id,
            'bus_line_id': bus_line.id,
            'departure_at': departure_at,
            'arrive_at': arrive_at,
        }
        serializer = BusTimetableSerializer(data=input_data)
        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    # 入力データのバリデーション（NG：name, codeが空文字）
    # db_constraint=False のため Error が発生しない

    def test_output_data(self):
        """出力データの内容検証"""
        bus_pair = BusPairFactory()
        bus_line = BusLineFactory()
        bus_pair_serializer = BusPairSerializer(
            instance=bus_pair)
        bus_line_serializer = BusLineSerializer(
            instance=bus_line)

        departure_at = FAKE.date_time(
            tzinfo=jst).strftime("%Y-%m-%d %H:%M:%S%z")
        arrive_at = FAKE.date_time(tzinfo=jst).strftime("%Y-%m-%d %H:%M%:%S%z")

        # シリアライザを作成
        bus_timetable = BusTimetable.objects.create(
            bus_pair=bus_pair,
            bus_line=bus_line,
            departure_at=departure_at,
            arrive_at=arrive_at
        )
        serializer = BusTimetableSerializer(instance=bus_timetable)

        # シリアライザの出力内容を検証
        expected_data = {
            'id': bus_timetable.id,
            'bus_pair': OrderedDict(bus_pair_serializer.data),
            'bus_line': OrderedDict(bus_line_serializer.data),
            'departure_at': departure_at,
            'arrive_at': arrive_at
        }

        self.assertDictEqual(serializer.data, expected_data)
