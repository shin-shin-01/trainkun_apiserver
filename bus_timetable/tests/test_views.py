from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import BusTimetable
from ..serializers import BusTimetableSerializer
from ..factories import BusTimetableFactory
from busstop.factories import BusstopFactory
from busstop.serializers import BusstopSerializer
from busstop.models import Busstop


class TestBusTimetableListCreateAPIView(APITestCase):
    """BusTimetableListCreateAPIViewのテストクラス"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.TARGET_URL = '/api/bus_timetables/'
        # ダミーのデータ作成
        cls.departure_bus_stop = BusstopFactory()
        cls.arrival_bus_stop = BusstopFactory()
        cls.departure_bus_stop_serializer = BusstopSerializer(
            instance=cls.departure_bus_stop)
        cls.arrival_bus_stop_serializer = BusstopSerializer(
            instance=cls.arrival_bus_stop)

    def test_create_success(self):
        """バス時刻モデル登録APIへのPOSTリクエスト（正常系）"""
        # APIリクエストを実行
        params = {
            'departure_bus_stop_id': self.departure_bus_stop.id,
            'arrival_bus_stop_id': self.arrival_bus_stop.id,
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusTimetable.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        bus_timetable = BusTimetable.objects.get()
        expected_json_dict = {
            'id': bus_timetable.id,
            'departure_bus_stop': self.departure_bus_stop_serializer.data,
            'arrival_bus_stop': self.arrival_bus_stop_serializer.data,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_bad_request_id_not_provided(self):
        """バス時刻モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG)"""
        # APIリクエストを実行
        params = {
            'departure_bus_stop_id': '',
            'arrival_bus_stop_id': self.arrival_bus_stop.id,
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusTimetable.objects.count(), 0)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

    def test_create_bad_request_invalid_id(self):
        """バス時刻モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG)"""
        invalid_id = Busstop.objects.count() + 1

        # APIリクエストを実行
        params = {
            'departure_bus_stop_id': invalid_id,
            'arrival_bus_stop_id': self.arrival_bus_stop.id,
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
        cls.bus_timetable_serializer = BusTimetableSerializer(cls.bus_timetable)

    def test_get_success(self):
        """バス時刻モデル取得（詳細）APIへのGETリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(
                self.bus_timetable.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.bus_timetable_serializer.data)

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
