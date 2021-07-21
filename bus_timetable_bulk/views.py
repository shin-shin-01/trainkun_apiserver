import json
from typing import Union, List, Dict
from logging import captureWarnings
from rest_framework import status, views
from rest_framework.response import Response

from bus_pair.models import BusPair
from bus_line.models import BusLine
from bus_timetable.models import BusTimetable
from bus_timetable.serializers import BusTimetableSerializer
# スクレイピング用関数
from .scraping import scraping


class BusTimetableBulkCreateAPIView(views.APIView):
    """バス停時刻表を一度に登録するAPIクラス"""

    """
    data = {
        "bus_pair_id": 1,
        "bus_line_id": 1,
    }
    """

    def post(self, request, *args, **kwargs):
        # BusPairFactory(id=1)
        data = json.loads(request.body)

        busstop_codes = get_busstop_codes(data)
        bus_line_code = get_bus_line_code(data)
        if busstop_codes is None or bus_line_code is None:
            Response(status.HTTP_400_BAD_REQUEST)

        # 時刻表を取得
        timetable_list: List[Dict[str, str]] = scraping(
            busstop_codes, bus_line_code)
        bus_timetable_objects: List[BusTimetable] = []
        for timetable in timetable_list:
            bus_timetable_objects.append(
                BusTimetable(
                    bus_pair_id=data["bus_pair_id"],
                    bus_line_id=data["bus_line_id"],
                    arrive_at=timetable["arrive_at"],
                    departure_at=timetable["departure_at"]
                )
            )
        BusTimetable.objects.bulk_create(bus_timetable_objects)
        return Response(status.HTTP_200_OK)


# バス停組み合わせIDから 出発 / 到着 バス停を取得
def get_busstop_codes(data: Dict[str, str]) -> Union[Dict[str, str], None]:
    try:
        bus_pair_id = data["bus_pair_id"]
        bus_pair = BusPair.objects.get(id=bus_pair_id)
        return {
            "departure_busstop_code": bus_pair.departure_busstop.code,
            "arrive_busstop_code": bus_pair.arrive_busstop.code
        }
    except KeyError:
        return None
    except BusPair.DoesNotExist:
        return None

# バス停路線IDから バス路線コードを取得


def get_bus_line_code(data: Dict[str, str]) -> Union[str, None]:
    try:
        bus_line_id = data["bus_line_id"]
        bus_line = BusLine.objects.get(id=bus_line_id)
        return bus_line.code
    except KeyError:
        return None
    except BusLine.DoesNotExist:
        return None
