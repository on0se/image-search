import faiss
import numpy as np

from searcher import add_index, faiss_search

DIM = 768  # DINOv2 vitb14 の出力次元

def vec(seed):
    """再現性のある乱数ベクトル。DINOv2 は動かさない"""
    return np.random.default_rng(seed).random((1, DIM), dtype=np.float32)

def build(n):
    index = None
    for i in range(n):
        index = add_index(vec(i), index)
    return index

def test_初回はHNSWインデックスが作られる():
    """総当たりではなくHNSWを使う（docs/design.md §3）"""
    assert isinstance(build(1), faiss.IndexHNSWFlat)

def test_次元はベクトルから決まる():
    assert build(1).d == DIM

def test_追加するたびに件数が増える():
    """HNSWは差分追加できる（docs/design.md §3）"""
    index = None
    for i in range(3):
        index = add_index(vec(i), index)
        assert index.ntotal == i + 1

def test_返り値はtopk件の添え字():
    results = faiss_search(build(5), vec(0), 3)
    assert len(results) == 3
    assert all(isinstance(r, int) for r in results)
    assert all(0 <= r < 5 for r in results)

def test_件数より多く要求すると足りない分はマイナス1になる():
    """
    main.py の topK = min(topK, repo.count()) が必要な理由。
    このガードを外すと -1 が添え字として返り、呼び出し側が壊れる
    """
    results = faiss_search(build(2), vec(0), 5)
    assert len(results) == 5
    assert results.count(-1) == 3
