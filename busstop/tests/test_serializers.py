from django.test import TestCase
from django.utils.timezone import localtime
from rest_framework import serializers

from ..models import Busstop
from ..serializers import BusstopSerializer

class TEstBusstopSerializer(TestCase):
    """BusstopSerializerのテストクラス"""

    def test_input_valid(self):
        """入力データのバリデーション（OK）"""
        # シリアライザを作成
        input_data = {
            'name': 'name',
            'code': '00000000',
        }
        serializer = BusstopSerializer(data=input_data)
        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), True)

    def test_input_invalid_if_required_params_is_blank(self):
        """入力データのバリデーション（NG：name, codeが空文字）"""
        # シリアライザを作成
        input_data = {
            'name': '',
            'code': '',
        }
        serializer = BusstopSerializer(data=input_data)
        # バリデーションの結果を検証
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(serializer.errors.keys(), ['name', 'code'])
        self.assertCountEqual(
            [str(x) for x in serializer.errors['name']],
            ["This field may not be blank."],
        )
        self.assertCountEqual(
            [str(x) for x in serializer.errors['code']],
            ["This field may not be blank."],
        )

    def test_output_data(self):
        """出力データの内容検証"""
        # シリアライザを作成
        busstop = Busstop.objects.create(
            name='name',
            code='00000000',
        )
        serializer = BusstopSerializer(instance=busstop)
        # シリアライザの出力内容を検証
        expected_data = {
            'id': busstop.id,
            'name': busstop.name,
            'code': busstop.code,
        }
        self.assertDictEqual(serializer.data, expected_data)
