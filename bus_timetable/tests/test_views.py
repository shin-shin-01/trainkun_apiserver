from django.utils.timezone import localtime
from rest_framework.test import APITestCase
from factory.faker import faker
from datetime import timedelta, timezone
from json import loads, dumps

from ..models import BusTimetable
from ..serializers import BusTimetableSerializer
from ..factories import BusTimetableFactory
from bus_pair.factories import BusPairFactory
from bus_line.factories import BusLineFactory
from bus_pair.serializers import BusPairSerializer
from bus_line.serializers import BusLineSerializer
from bus_pair.models import BusPair

FAKE = faker.Faker()
JST = timezone(timedelta(hours=+9), 'JST')


class TestBusTimetableListCreateAPIView(APITestCase):
    """BusTimetableListCreateAPIViewのテストクラス"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TARGET_URL = '/api/bus_timetables/'
        # ダミーのデータ作成
        cls.bus_pair = BusPairFactory()
        cls.bus_line = BusLineFactory()
        cls.bus_pair_serializer = BusPairSerializer(
            instance=cls.bus_pair)
        cls.bus_line_serializer = BusLineSerializer(
            instance=cls.bus_line)
        cls.departure_at = FAKE.date_time(tzinfo=JST).isoformat()
        cls.arrive_at = FAKE.date_time(tzinfo=JST).isoformat()

    def test_create_success(self):
        """バス時刻モデル登録APIへのPOSTリクエスト（正常系）"""
        # APIリクエストを実行
        params = {
            'bus_pair_id': self.bus_pair.id,
            'bus_line_id': self.bus_line.id,
            'departure_at': self.departure_at,
            'arrive_at': self.arrive_at,
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusTimetable.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        bus_timetable = BusTimetable.objects.get()
        expected_json_dict = {
            'id': bus_timetable.id,
            'bus_pair': loads(dumps(self.bus_pair_serializer.data)),
            'bus_line': self.bus_line_serializer.data,
            'departure_at': self.departure_at,
            'arrive_at': self.arrive_at
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_bad_request_id_not_provided(self):
        """バス時刻モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG)"""
        # APIリクエストを実行
        params = {
            'bus_pair_id': '',
            'bus_line_id': self.bus_line.id,
            'departure_at': self.departure_at,
            'arrive_at': self.arrive_at,
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusTimetable.objects.count(), 0)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

    def test_create_bad_request_invalid_id(self):
        """バス時刻モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG)"""
        invalid_id = BusPair.objects.count() + 1

        # APIリクエストを実行
        params = {
            'bus_pair_id': invalid_id,
            'bus_line_id': self.bus_line.id,
            'departure_at': self.departure_at,
            'arrive_at': self.arrive_at,
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusTimetable.objects.count(), 0)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

    def test_get_success(self):
        """バス時刻モデル取得APIへのGETリクエスト（正常系）"""
        # ダミーのデータ作成
        BusTimetableFactory()
        # APIリクエスト
        response = self.client.get(self.TARGET_URL, format='json')
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        bus_timetable = BusTimetable.objects.get()
        busstop_serializer = BusTimetableSerializer(bus_timetable)
        self.assertJSONEqual(response.content, [busstop_serializer.data])


class TestBusTimetableRetrieveUpdateDestroyAPIView(APITestCase):
    """BusTimetableRetrieveUpdateDestroyAPIViewのテストクラス"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TARGET_URL_WITH_PK = '/api/bus_timetables/{}/'
        # ダミーのデータ作成
        cls.bus_timetable = BusTimetableFactory()
        cls.bus_timetable_serializer = BusTimetableSerializer(
            cls.bus_timetable)

    def test_get_success(self):
        """バス時刻モデル取得（詳細）APIへのGETリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(
                self.bus_timetable.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            self.bus_timetable_serializer.data)

    def test_get_not_found(self):
        """バス時刻モデル取得（詳細）APIへのGETリクエスト（異常系：対象のバス時刻レコードが存在しない）"""
        # APIリクエスト
        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(
                self.bus_timetable.id + 1), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 404)

    # TODO: バス時刻モデル更新APIへのリクエスト テスト実装

    def test_delete_success(self):
        """バス時刻モデル削除APIへのPUTリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.delete(
            self.TARGET_URL_WITH_PK.format(
                self.bus_timetable.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 204)
        # データベースの状態を検証
        self.assertEqual(BusTimetable.objects.count(), 0)
