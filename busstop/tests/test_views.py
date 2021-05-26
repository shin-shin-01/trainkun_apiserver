from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import Busstop
from ..serializers import BusstopSerializer
from ..factories import BusstopFactory

class TestBusstopListCreateAPIView(APITestCase):
    """BusstopListCreateAPIViewのテストクラス"""
    
    TARGET_URL = '/api/busstops/'

    def test_create_success(self):
        """バス停モデル登録APIへのPOSTリクエスト（正常系）"""
        # APIリクエストを実行
        params = {
            'name': "name",
            'code': "00000000",
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(Busstop.objects.count(), 1)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 201)
        busstop = Busstop.objects.get()
        expected_json_dict = {
            'id': busstop.id,
            'name': busstop.name,
            'code': busstop.code,
            # 'created_at': str(localtime(busstop.created_at)).replace(' ', 'T'),
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create_bad_request(self):
        """バス停モデルの登録APIへのPOSTリクエスト（異常系：バリデーションNG)"""
        # APIリクエストを実行
        params = {
            'name': '',
            'code': '00000000',
        }
        response = self.client.post(self.TARGET_URL, params, format='json')
        # データベースの状態を検証
        self.assertEqual(Busstop.objects.count(), 0)
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 400)

    def test_get_success(self):
        """バス停モデル取得APIへのGETリクエスト（正常系）"""
        # ダミーのデータ作成
        BusstopFactory()
        # APIリクエスト
        response = self.client.get(self.TARGET_URL, format='json')
        # レスポンスの内容を検証
        self.assertEqual(response.status_code, 200)
        busstop = Busstop.objects.get()
        busstop = BusstopSerializer(busstop)
        self.assertJSONEqual(response.content, [busstop.data])

class TestBusstopRetrieveUpdateDestroyAPIView(APITestCase):
    """BusstopRetrieveUpdateDestroyAPIViewのテストクラス"""

    TARGET_URL_WITH_PK = '/api/busstops/{}/'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # ダミーのデータ作成
        cls.busstop = BusstopFactory()
        cls.busstop_serializer = BusstopSerializer(cls.busstop)

    def test_get_success(self):
        """バス停モデル取得（詳細）APIへのGETリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.get(self.TARGET_URL_WITH_PK.format(self.busstop.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, self.busstop_serializer.data)

    def test_get_not_found(self):
        """バス停モデル取得（詳細）APIへのGETリクエスト（異常系：対象のバス停レコードが存在しない）"""
        # APIリクエスト
        response = self.client.get(self.TARGET_URL_WITH_PK.format(self.busstop.id + 1), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 404)

    def test_part_update_success(self):
        """バス停モデル一部更新APIへのPUTリクエスト（正常系）"""
        params = {
            'name': 'new_name'
        }
        # APIリクエスト
        response = self.client.patch(self.TARGET_URL_WITH_PK.format(self.busstop.id), params, format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        expected_json_dict = {
            'id': self.busstop.id,
            'name': params['name'],
            'code': str(self.busstop.code),
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_all_update_success(self):
        """バス停モデル更新APIへのPUTリクエスト（正常系）"""
        params = {
            'name': 'new_name',
            'code': 'new_code',
        }
        # APIリクエスト
        response = self.client.put(self.TARGET_URL_WITH_PK.format(self.busstop.id), params, format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 200)
        expected_json_dict = {
            'id': self.busstop.id,
            'name': params['name'],
            'code': params['code'],
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_part_update_bad_request(self):
        """バス停モデル一部更新APIへのPUTリクエスト（異常系：バリデーションNG）"""
        params = {
            'name': ''
        }
        # APIリクエスト
        response = self.client.patch(self.TARGET_URL_WITH_PK.format(self.busstop.id), params, format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        """バス停モデル削除APIへのPUTリクエスト（正常系）"""
        # APIリクエスト
        response = self.client.delete(self.TARGET_URL_WITH_PK.format(self.busstop.id), format='json')
        # レスポンスの内容検証
        self.assertEqual(response.status_code, 204)
        # データベースの状態を検証
        self.assertEqual(Busstop.objects.count(), 0)
