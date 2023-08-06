from postodon import select_post
import pytest


test_string1 = [
    {"content": "Posted 1", "id": 0, "status": "posted"},
    {"content": "Posted 2", "id": 1, "status": "posted"},
    {"content": "Unposted 1", "id": 2, "status": "unposted"},
]
test_string2 = [
    {"content": "Unposted 1", "id": 0, "status": "unposted"},
]
test_string3 = [
    {"content": "Posted 1", "id": 0, "status": "posted"},
]
test_string4 = []
test_list1 = [0]
test_list2 = [10]
test_list3 = [0, 10]


@pytest.mark.parametrize(
    "data,status,reference",
    [
        (test_string1, "unposted", [2]),
        (test_string2, "unposted", [0]),
        (test_string3, "unposted", []),
        (test_string4, "unposted", []),
        (test_string1, "posted", [0, 1]),
        (test_string2, "posted", []),
        (test_string3, "posted", [0]),
        (test_string4, "posted", []),
    ],
)
def test_get_candidates(data, status, reference):
    assert select_post.get_candidates(data, status) == reference


# ---


@pytest.mark.parametrize(
    "candidates,reference",
    [
        (test_list1, [0]),
        (test_list2, [10]),
        (test_list3, [0, 10]),
    ],
)
def test_select_post_from(candidates, reference):
    result = select_post.select_post_from(candidates)
    assert type(result) == int
    assert result in reference
    if len(reference) == 1:
        assert result == reference[0]


# ---


@pytest.mark.parametrize(
    "data,selected_id,reference",
    [
        (test_string1, 0, 0),
        (test_string1, 1, 1),
        (test_string1, 2, 2),
        (test_string2, 0, 0),
        (test_string3, 0, 0),
    ],
)
def test_get_index_from_id(data, selected_id, reference):
    result = select_post.get_index_from_id(data, selected_id)
    assert result == reference


# ---


@pytest.mark.parametrize(
    "i,o1",
    [
        (test_string1, "Unposted 1"),
        (test_string2, "Unposted 1"),
        (test_string3, "Posted 1"),
    ],
)
def test_get_post(i, o1):
    assert select_post.get_post(i) == o1
