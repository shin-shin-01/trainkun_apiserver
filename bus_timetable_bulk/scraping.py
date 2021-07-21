from typing import Dict, List
import requests
import bs4


def scraping(busstop_codes: Dict[str, str],
             bus_line_code: str) -> List[Dict[str, str]]:
    url = f"https://www.navitime.co.jp/bus/diagram/timelist?departure={busstop_codes['departure_busstop_code']}&arrival={busstop_codes['arrive_busstop_code']}&line={bus_line_code}"

    site = requests.get(url)
    data = bs4.BeautifulSoup(site.text, "html.parser")
    data_time_details: bs4.element.ResultSet = data.find_all(
        class_="time-detail")

    results: List[Dict[str, str]] = []

    for time_detail in data_time_details:
        time_detail_list: List[str] = time_detail.text.split()

        if time_detail_list[0] == "（始）":
            del time_detail_list[0]  # 始発の場合に削除

        departure_at = time_detail_list[0]
        arrive_at = time_detail_list[1]
        results.append(
            {
                "departure_at": departure_at[:-1],
                "arrive_at": arrive_at[:-1]
            }
        )
    return results


# テスト用実行
if __name__ == "__main__":
    # データ準備
    busstop_codes = {
        # - 九大学研都市
        "departure_busstop_code": "00291944",
        # - 産学連携交流センター
        "arrive_busstop_code": "00087909",
    }
    # - 九州大学線〔学園通経由〕[昭和バス]
    bus_line_code = "00053907"

    results = scraping(busstop_codes, bus_line_code)

    # [{'departure_at': '07:35', 'arrive_at': '07:44'}, {'departure_at': '07:48', 'arrive_at': '07:57'},
    print(results)
