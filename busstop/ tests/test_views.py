from django.utils.timezone import localtime
from rest_framework.test import APITestCase

from ..models import Busstop

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
            'id': str(busstop.id),
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
