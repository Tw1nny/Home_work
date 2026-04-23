from src.processing import filter_by_state, sort_by_date


def test_filter_by_state():
    data = [
        {"state": "EXECUTED", "id": 1},
        {"state": "CANCELED", "id": 2},
        {"state": "EXECUTED", "id": 3},
    ]
    assert filter_by_state(data) == [{"state": "EXECUTED", "id": 1}, {"state": "EXECUTED", "id": 3}]
    assert filter_by_state(data, "CANCELED") == [{"state": "CANCELED", "id": 2}]


def test_sort_by_date():
    data = [
        {"date": "2019-07-03T18:35:29.512364", "id": 1},
        {"date": "2018-06-30T02:08:58.425572", "id": 2},
        {"date": "2020-01-01T00:00:00", "id": 3},
    ]
    sorted_desc = sort_by_date(data)
    assert [d["id"] for d in sorted_desc] == [3, 1, 2]
    sorted_asc = sort_by_date(data, descending=False)
    assert [d["id"] for d in sorted_asc] == [2, 1, 3]
