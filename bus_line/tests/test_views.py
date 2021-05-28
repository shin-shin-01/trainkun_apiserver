from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import BusLine
from ..serializers import BusLineSerializer
from ..factories import BusLineFactory


class TestBusLineListCreateAPIView(APITestCase):
    """BusLineListCreateAPIViewのテストクラス"""

    TARGET_URL = '/api/bus_lines/'

    def test_create_success(self):
        """バス路線モデル登録APIへのPOSTリクエスト（正常系）"""
        # APIリクエストを実行
        params = {
            'name': "name",
            'code': "00000000",
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusLine.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        bus_line = BusLine.objects.get()
        expected_json_dict = {
            'id': bus_line.id,
            'name': bus_line.name,
            'code': bus_line.code,
            # 'created_at': str(localtime(bus_line.created_at)).replace(' ', 'T'),
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_bad_request(self):
        """バス路線モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG)"""
        # APIリクエストを実行
        params = {
            'name': '',
            'code': '00000000',
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(BusLine.objects.count(), 0)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

    def test_get_success(self):
        """バス路線モデル取得APIへのGETリクエスト（正常系）"""
        # ダミーのデータ作成
        BusLineFactory()
        # APIリクエスト
        response = self.client.get(self.TARGET_URL, format='json')
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        bus_line = BusLine.objects.get()
        busstop_serializer = BusLineSerializer(bus_line)
        self.assertJSONEqual(response.content, [busstop_serializer.data])


class TestBusLineRetrieveUpdateDestroyAPIView(APITestCase):
    """BusLineRetrieveUpdateDestroyAPIViewのテストクラス"""

    TARGET_URL_WITH_PK = '/api/bus_lines/{}/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # ダミーのデータ作成
        cls.bus_line = BusLineFactory()
        cls.bus_line_serializer = BusLineSerializer(cls.bus_line)

    def test_get_success(self):
        """バス路線モデル取得（詳細）APIへのGETリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(
                self.bus_line.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.bus_line_serializer.data)

    def test_get_not_found(self):
        """バス路線モデル取得（詳細）APIへのGETリクエスト（異常系：対象のバス路線レコードが存在しない）"""
        # APIリクエスト
        response = self.client.get(
            self.TARGET_URL_WITH_PK.format(
                self.bus_line.id + 1), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 404)

    def test_part_update_success(self):
        """バス路線モデル一部更新APIへのPUTリクエスト（正常系）"""
        params = {
            'name': 'new_name'
        }
        # APIリクエスト
        response = self.client.patch(
            self.TARGET_URL_WITH_PK.format(
                self.bus_line.id), params, format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        expected_json_dict = {
            'id': self.bus_line.id,
            'name': params['name'],
            'code': str(self.bus_line.code),
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_all_update_success(self):
        """バス路線モデル更新APIへのPUTリクエスト（正常系）"""
        params = {
            'name': 'new_name',
            'code': 'new_code',
        }
        # APIリクエスト
        response = self.client.put(
            self.TARGET_URL_WITH_PK.format(
                self.bus_line.id), params, format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        expected_json_dict = {
            'id': self.bus_line.id,
            'name': params['name'],
            'code': params['code'],
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_part_update_bad_request(self):
        """バス路線モデル一部更新APIへのPUTリクエスト（異常系：バリデーションNG）"""
        params = {
            'name': ''
        }
        # APIリクエスト
        response = self.client.patch(
            self.TARGET_URL_WITH_PK.format(
                self.bus_line.id), params, format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        """バス路線モデル削除APIへのPUTリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.delete(
            self.TARGET_URL_WITH_PK.format(
                self.bus_line.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 204)
        # データベースの状態を検証
        self.assertEqual(BusLine.objects.count(), 0)
