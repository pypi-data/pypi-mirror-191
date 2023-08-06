from indra import api
from .constants import (
    COCO_DS_NAME,
    MNIST_DS_NAME,
    IMAGENET_DS_NAME,
)
from .utils import tmp_datasets_dir
import deeplake
import numpy as np
import math

from time import time
import pytest


@pytest.mark.parametrize(
    "ds_name,queries",
    [
        (
            COCO_DS_NAME,
            [
                ("select * sample by max_weight(any(categories == 'person'): 10, True: 0.1)", 118287, None),
                ("select * sample by max_weight(contains(categories, 'person'): 10, True: 0.1)", 118287, None),
                ("select * where not contains(categories, 'truck')", 112160, None),
                ("SELECT * WHERE categories[0] == 'person'", 22497, None),
                ("SELECT * WHERE shape(categories)[0] == 0", 1021, None),
                ("SELECT * WHERE shape(boxes)[0] == 5", 7712, None),
                ("SELECT * WHERE shape(images)[0] > 200", 118078, None),
                ("SELECT * WHERE shape(images)[1] > 200", 118219, None),
                ("SELECT * WHERE shape(images)[2] == 3", 118060, None),
                ("SELECT * WHERE shape(images)[2] == 2", 0, None),
                (
                    "SELECT * WHERE ALL_STRICT(categories == 'person') or shape(categories)[0] == 0",
                    1375,
                    None,
                ),
                ("SELECT * WHERE ALL(categories == 'person')", 1375, None),
                ("select * where ALL_STRICT(categories == 'person')", 354, None),
                (
                    "select * where ALL_STRICT(\"pose/categories\" == 'person')",
                    64115,
                    None,
                ),
                ("select * where any(categories == 'banana')", 2243, None),
                ("select * where any(categories == 'person')", 64115, None),
                (
                    "select * where all_strict(logical_and(categories == 2, boxes[:,3] > 200))",
                    5,
                    None,
                ),
                (
                    "select * where all_strict(logical_and(categories == 'car', boxes[:,3] > 200))",
                    5,
                    None,
                ),
                (
                    "select * where any(logical_and(categories == 'car', boxes[:,3] > 200))",
                    1242,
                    None,
                ),
                (
                    "select * where all_strict(logical_or(categories == 'person', categories == 'banana'))",
                    873,
                    None,
                ),
                (
                    "select * where all(logical_and(categories == 'person', categories == 'person'))",
                    1375,
                    None,
                ),
                ("SELECT * where images_meta['license'] == 3", 32184, None),
                ("SELECT * where images_meta['id'] > 285529", 60365, None),
                ("SELECT * where contains(categories, '*ers*')", 64115, None),
                ("SELECT * where contains(categories, '?ers*')", 64115, None),
                (
                    "SELECT * ORDER BY shape(boxes)[0] limit 100",
                    100,
                    [
                        42,
                        92,
                        224,
                        302,
                        415,
                        693,
                        699,
                        722,
                        750,
                        817,
                        852,
                        861,
                        1068,
                        1252,
                        1473,
                        1483,
                        1502,
                        1527,
                        1638,
                        1921,
                        1928,
                        1935,
                        1999,
                        2034,
                        2063,
                        2069,
                        2110,
                        2191,
                        2488,
                        2511,
                        2602,
                        2687,
                        2740,
                        3074,
                        3093,
                        3177,
                        3314,
                        3367,
                        3417,
                        4137,
                        4270,
                        4324,
                        4465,
                        4549,
                        4569,
                        4670,
                        4796,
                        4906,
                        4974,
                        5152,
                        5240,
                        5253,
                        5298,
                        5336,
                        5464,
                        5763,
                        5777,
                        5868,
                        5875,
                        5901,
                        5955,
                        6061,
                        6071,
                        6182,
                        6454,
                        6537,
                        6779,
                        6835,
                        6841,
                        6858,
                        6986,
                        7177,
                        7262,
                        7277,
                        7342,
                        7486,
                        7676,
                        7752,
                        7858,
                        7866,
                        7915,
                        8003,
                        8082,
                        8165,
                        8283,
                        8377,
                        8652,
                        8992,
                        9233,
                        9288,
                        9372,
                        9395,
                        9560,
                        9701,
                        9940,
                        10088,
                        10171,
                        10176,
                        10201,
                        10358,
                    ],
                ),
                ("SELECT * order by images_meta['license']", 118287, None),
                (
                    "SELECT * order by images_meta['license'] limit 100",
                    100,
                    [
                        1,
                        7,
                        20,
                        24,
                        25,
                        31,
                        37,
                        41,
                        42,
                        46,
                        48,
                        52,
                        53,
                        56,
                        59,
                        60,
                        61,
                        65,
                        70,
                        71,
                        72,
                        73,
                        75,
                        79,
                        80,
                        86,
                        89,
                        98,
                        99,
                        107,
                        111,
                        117,
                        119,
                        120,
                        127,
                        138,
                        140,
                        148,
                        150,
                        156,
                        158,
                        162,
                        164,
                        167,
                        171,
                        172,
                        180,
                        191,
                        200,
                        205,
                        207,
                        210,
                        211,
                        214,
                        217,
                        228,
                        229,
                        233,
                        234,
                        244,
                        245,
                        248,
                        252,
                        253,
                        262,
                        273,
                        276,
                        280,
                        283,
                        302,
                        313,
                        315,
                        320,
                        326,
                        331,
                        336,
                        337,
                        339,
                        349,
                        351,
                        352,
                        354,
                        355,
                        359,
                        370,
                        383,
                        388,
                        389,
                        392,
                        393,
                        399,
                        400,
                        406,
                        408,
                        409,
                        416,
                        419,
                        430,
                        431,
                        432,
                    ],
                ),
            ],
        ),
        (
            MNIST_DS_NAME,
            [
                ("SELECT * WHERE labels == 0", 5923, None),
                ("SELECT * WHERE SHAPE(images)[0] == 28", 60000, None),
                ("SELECT * WHERE SHAPE(images)[0] == 29", 0, None),
                ("select * sample by max_weight(any(labels == 1): 10, True: 1)", 60000, None),
                (
                    "(select * where labels == 4 limit 10) union (select * where labels == 5 limit 10) order by labels",
                    20,
                    [
                        2,
                        9,
                        20,
                        26,
                        53,
                        58,
                        60,
                        61,
                        64,
                        89,
                        0,
                        11,
                        35,
                        47,
                        65,
                        100,
                        132,
                        138,
                        145,
                        173,
                    ],
                ),
                (
                    "SELECT * SAMPLE BY sum_weight(labels == 0: 10, labels == 1: 5) LIMIT 100",
                    100,
                    None,
                ),
                (
                    "SELECT * SAMPLE BY max_weight(labels == 0: 10, labels == 1: 5) LIMIT 100",
                    100,
                    None,
                ),
                ("SELECT * SAMPLE BY labels", 60000, None),
                (
                    "SELECT * SAMPLE BY sum_weight(labels > 5: 1, labels == 0: 3) REPLACE LIMIT 10000",
                    10000,
                    None,
                ),
                (
                    "SELECT * SAMPLE BY max_weight(labels > 5: 1, labels == 0: 3) REPLACE LIMIT 10000",
                    10000,
                    None,
                ),
                ("SELECT * WHERE labels == 0 SAMPLE BY labels", 5923, None),
                ("SELECT * SAMPLE BY 1", 60000, None),
                ("SELECT * SAMPLE BY 0.1", 60000, None),
                ("SELECT * SAMPLE BY 0.1 LIMIT 30000", 30000, None),
                ("SELECT * SAMPLE BY 0.1 REPLACE FALSE LIMIT 190000", 60000, None),
                ("SELECT * SAMPLE BY 0.1 LIMIT 190000", 190000, None),
                ("SELECT * SAMPLE BY 0.1 REPLACE LIMIT 190000", 190000, None),
                ### TODO TQL (
                ###    "select * from(select * from (select *[0:10] from (select * group by labels) where shape(labels)[0] > 6000) ungroup by split) order by random()",
                ###    30,
                ###    None,
                ###),
            ],
        ),
        (
            IMAGENET_DS_NAME,
            [
                ("SELECT * WHERE labels == 'bikini'", 1300, None),
                ("SELECT * WHERE contains(labels, '*iki*')", 2600, None),
                ("SELECT * WHERE contains(labels, '?iki*')", 1300, None),
                ("SELECT * WHERE SHAPE(boxes)[0] > 15", 2, None),
                (
                    "(SELECT * WHERE labels == 'bikini' LIMIT 10) UNION (SELECT * WHERE labels == 1 LIMIT 10) UNION (SELECT * WHERE labels == 43 LIMIT 10)",
                    30,
                    None,
                ),
                ("select * sample by max_weight(contains(labels, 'banana'): 100, True: 0.1)", 1281166, None),
                (
                    "SELECT * SAMPLE BY sum_weight(labels == 'fur coat': 10, labels == 'bikini': 3) limit 0.1 PERCENT",
                    1281,
                    None,
                ),
                (
                    "SELECT * SAMPLE BY max_weight(labels == 'fur coat': 10, labels == 'bikini': 3) limit 0.1 PERCENT",
                    1281,
                    None,
                ),
                (
                    "SELECT * SAMPLE BY sum_weight(labels == 'fur coat': 10, labels == 'bikini': 3) replace",
                    1281166,
                    None,
                ),
                (
                    "SELECT * SAMPLE BY sum_weight(labels == 'fur coat': 10, labels == 'bikini': 3) replace",
                    1281166,
                    None,
                ),
                (
                    "SELECT * SAMPLE BY max_weight(labels == 'fur coat': 10, True: 0.1)",
                    1281166,
                    None,
                ),
            ],
        ),
        # LAION_400_M_DS_NAME: [
        #    ("SELECT * WHERE CONTAINS(caption, 'blue')", 2783, None),
        #    ("SELECT * WHERE caption[0] == 'A'", 28904, None),
        #    ("SELECT * WHERE SHAPE(image)[0] == 256", 512993, None),
        # ],
        (
            "hub://davitbun/places365-train-challenge",
            [
                ("SELECT * WHERE labels == 'hotel_room'", 32947, None),
                ("SELECT * ORDER by random()", 8026628, None),
            ],
        ),
    ],
)
def test_dataset_query_results(ds_name, queries):
    ds = api.dataset(ds_name)
    for (query, result_size, result_indices) in queries:
        print(f"\tRunning query: {query}")
        start = time()
        result = ds.query(query)
        print("\tQuery time: ", time() - start)
        assert len(result) == result_size
        assert result_indices is None or result.indexes == result_indices
        start = time()
        result = ds.query(query)
        print("\tSecond Query time: ", time() - start)

"""
TODO TQL
def test_nested_queries():
    ds = api.dataset(MNIST_DS_NAME)
    dsv = ds.query("SELECT * WHERE labels < 4")
    dsv2 = dsv.query("SELECT * WHERE labels > 2")
    assert len(dsv2) == 6131
"""

def test_query_order_by_array_error(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / "query_order_by_array", overwrite=True)
    with ds:
        ds.create_tensor("boxes", dtype=np.uint8, htype="bbox")
        ds.boxes.append([0, 1, 2, 3])
        ds.boxes.append([1, 2, 10, 2])
        ds.boxes.append([10, 2, 10, 2])
        ds.boxes.append([5, 2, 10, 2])
    ids = api.dataset(str(tmp_datasets_dir / "query_order_by_array"))
    thrown = False
    try:
        view = ids.query("SELECT * order by boxes")
    except Exception as e:
        thrown = True
    assert thrown

"""
TODO TQL
def test_query_group_by_result_access(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / "query_group_by_access", overwrite=True)
    with ds:
        ds.create_tensor("image", dtype=np.uint8, max_chunk_size=10*1024, htype="image", sample_compression=None)
        for i in range(1000):
            ds.image.append(np.random.randint(0, 255, (28, 28, 1), np.uint8))
        ds.create_tensor("label", dtype=np.int32, htype="class_label")
        for i in range(1000):
            ds.label.append(i % 4)
    ids = api.dataset(str(tmp_datasets_dir / "query_group_by_access"))
    view = ids.query("SELECT * group by label")
    assert len(view) == 4
    for i in range(4):
        assert len(view.tensors[0][i]) == 250
        for j in range(250):
            assert np.all(view.tensors[0][i][j] == ds.image[4 * j + i].numpy())
"""

def test_polygon_query(tmp_datasets_dir):
    ds = deeplake.dataset(tmp_datasets_dir / "polygon_dataset", overwrite=True)
    with ds:
        ds.create_tensor(
            "polygon",
            dtype=np.float32,
            htype="polygon",
            sample_compression=None,
        )
        ds.create_tensor(
            "image",
            dtype=np.uint8,
            htype="image",
            sample_compression="jpeg",
        )
        for i in range(10):
            polygons = []
            for j in range(i):
                p = np.ndarray((3 + j, 2))
                c = (3 + j) / 2
                for k in range(3 + j):
                    p[k] = [200 * (j % 3) + 150 * (math.sin(6.28 * k / (3 + j)) + 1) / 2, 200 * (j / 3) + 150 * (math.cos(6.28 * k / (3 + j)) + 1) / 2]
                polygons.append(p)
            ds.polygon.append(polygons)
            ds.image.append(np.zeros((600, 600, 3), np.uint8))


    ids = api.dataset(str(tmp_datasets_dir / "polygon_dataset"))
    dsv = ids.query("SELECT * WHERE any(polygon[:,:,0] > 300)")
    assert len(dsv) == 8
    dsv = ids.query("SELECT * WHERE all(polygon[:,:,0] < 300)")
    assert len(dsv) == 2
    dsv = ids.query("SELECT * WHERE all(polygon[:,:,1] < 300)")
    assert len(dsv) == 4
    dsv = ids.query("SELECT * WHERE all(polygon[:,:,1] > 0)")
    assert len(dsv) == 10
