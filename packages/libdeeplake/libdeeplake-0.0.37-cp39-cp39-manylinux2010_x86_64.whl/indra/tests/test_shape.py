from indra import api
from indra.pytorch.loader import Loader
from .constants import MNIST_DS_NAME, COCO_DS_NAME
import numpy as np
import deeplake
import pickle
import shutil
from deeplake.util.exceptions import TokenPermissionError
import pytest
from .utils import tmp_datasets_dir

def test_ordinary_shape(tmp_datasets_dir):
    tmp_ds = deeplake.dataset(tmp_datasets_dir / "shape_test_dataset", overwrite=True)
    with tmp_ds as ds:
        ds.create_tensor("labels", htype="class_label")
        ds.create_tensor("images", htype="image", sample_compression="jpeg")
        ds.labels.append([1, 2, 3])
        ds.labels.append([1])
        ds.images.append(np.random.randint(0, 255, (400, 600, 3), np.uint8))
        ds.images.append(np.random.randint(0, 255, (200, 300, 3), np.uint8))

    ds2 = api.dataset(str(tmp_datasets_dir / "shape_test_dataset"))
    assert len(ds2) == 2
    assert ds2.tensors[0].name == "labels"
    assert ds2.tensors[0].shape(0) == [3]
    assert ds2.tensors[0].shape(1) == [1]
    assert ds2.tensors[1].name == "images"
    assert ds2.tensors[1].shape(0) == [400, 600, 3]
    assert ds2.tensors[1].shape(1) == [200, 300, 3]

def test_dynamic_shape(tmp_datasets_dir):
    tmp_ds = deeplake.dataset(tmp_datasets_dir / "shape_test_dataset_sequential", overwrite=True)
    with tmp_ds as ds:
        ds.create_tensor("labels", htype="sequence[class_label]")
        ds.create_tensor("images", htype="sequence[image]", sample_compression="jpeg")
        ds.labels.append([[1, 2, 3], [1], [2, 3]])
        ds.labels.append([[1, 2, 3, 2, 1]])
        a = list()
        for i in range(5):
            a.append(np.random.randint(0, 255, (400, 600, 3), np.uint8))
        ds.images.append(a)

    ds2 = api.dataset(str(tmp_datasets_dir / "shape_test_dataset_sequential"))
    assert ds2.tensors[0].shape(0) == [[3], [1], [2]]
    assert ds2.tensors[0].shape(1) == [[5]]
    assert ds2.tensors[1].shape(0) == [[400, 600, 3], [400, 600, 3], [400, 600, 3], [400, 600, 3], [400, 600, 3]]
