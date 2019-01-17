import pytest

import numpy as np

import fastremap

DTYPES = (
  np.uint8, np.uint16, np.uint32, np.uint64,
  np.int8, np.int16, np.int32, np.int64
)

def test_empty_renumber():
  for dtype in DTYPES:
    data = np.array([], dtype=dtype)
    data2, remapdict = fastremap.renumber(data, preserve_zero=False)

    assert np.all(data2 == [])
    assert remapdict == {}

def test_1d_renumber():
  for dtype in DTYPES:
    data = np.arange(8).astype(dtype)
    data = np.flip(data)

    data2 = np.copy(data)
    data2, remapdict = fastremap.renumber(data2, preserve_zero=False)

    assert np.all(data2 == np.arange(1,9))
    assert len(remapdict) > 0

    data2 = np.copy(data)
    data2, remapdict = fastremap.renumber(data2, preserve_zero=True)

    assert data2[-1] == 0
    assert np.all(data2 == [1,2,3,4,5,6,7,0])
    assert len(remapdict) > 0

  data = np.arange(8).astype(np.bool)
  data = np.flip(data)

  data2 = np.copy(data)
  data2, remapdict = fastremap.renumber(data2, preserve_zero=False)

  assert np.all(data2 == [1,1,1,1,1,1,1,2])
  assert len(remapdict) > 0

  data2 = np.copy(data)
  data2, remapdict = fastremap.renumber(data2, preserve_zero=True)

  assert np.all(data2 == [1,1,1,1,1,1,1,0])
  assert len(remapdict) > 0

def test_2d_renumber():
  for dtype in DTYPES:
    data = np.array([
      [ 5,  5,  5, 2],
      [ 3,  5,  5, 0],
      [ 1,  2,  4, 1],
      [20, 19, 20, 1],
    ], dtype=dtype)

    data2 = np.copy(data, order='C')
    data2, remapdict = fastremap.renumber(data2, preserve_zero=True)

    assert np.all(data2 == [
      [1, 1, 1, 2],
      [3, 1, 1, 0],
      [4, 2, 5, 4],
      [6, 7, 6, 4],
    ])

    data2 = np.copy(data, order='F')
    data2, remapdict = fastremap.renumber(data2, preserve_zero=True)

    assert np.all(data2 == [
      [1, 1, 1, 5],
      [2, 1, 1, 0],
      [3, 5, 7, 3],
      [4, 6, 4, 3],
    ])

def test_3d_renumber():
  big = 9999999999
  data = np.array([
    [
      [big, 0],
      [2, big],
    ],
    [
      [big*2, big-1],
      [big*3, big-3],
    ],
  ], dtype=np.uint64)

  data2 = np.copy(data, order='C')
  data2, remapdict = fastremap.renumber(data2, preserve_zero=True)

  assert np.all(data2 == [
    [
      [1, 0],
      [2, 1]
    ],
    [ 
      [3, 4],
      [5, 6],
    ],
  ])

  data2 = np.copy(data, order='F')
  data2, remapdict = fastremap.renumber(data2, preserve_zero=True)

  assert np.all(data2 == [
    [
      [1, 0],
      [3, 1]
    ],
    [ 
      [2, 5],
      [4, 6],
    ],
  ])


