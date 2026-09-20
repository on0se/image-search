import numpy as np
from PIL import Image
import pytest

from preprocess import pad_to_square, trans_to_dinov2

# 黒帯と区別するため、背景の黒とは違う色を使う
SUBJECT = (10, 200, 100)

def make(w, h):
    return Image.new("RGB", (w, h), SUBJECT)

@pytest.mark.parametrize("w,h", [(200, 400), (400, 200), (300, 300)])
def test_出力は正方形になる(w, h):
    out = pad_to_square(make(w, h))
    assert out.size[0] == out.size[1]

@pytest.mark.parametrize("w,h", [(200, 400), (400, 200), (300, 300)])
def test_辺の長さは長辺に一致する(w, h):
    out = pad_to_square(make(w, h))
    assert out.size == (max(w, h), max(w, h))

@pytest.mark.parametrize("w,h", [(200, 400), (400, 200), (300, 300), (201, 400), (400, 201)])
def test_元画像が欠けない(w, h):
    """
    パディングは情報を落とさない（docs/design.md §2）
    中心切り出しを採らなかった根拠そのもの
    """
    out = pad_to_square(make(w, h))
    kept = int((np.asarray(out) == SUBJECT).all(axis=2).sum())
    assert kept == w * h

@pytest.mark.parametrize("w,h", [(200, 400), (400, 200), (201, 400)])
def test_元画像は中心に置かれる(w, h):
    out = pad_to_square(make(w, h))
    left, top, right, bottom = out.getbbox()
    side = max(w, h)
    # 割り切れない場合は // 2 の切り捨てで1pxずれる
    assert abs(left - (side - right)) <= 1
    assert abs(top - (side - bottom)) <= 1

@pytest.mark.parametrize("w,h", [(200, 400), (400, 200), (300, 300)])
def test_DINOv2への入力は3x224x224になる(w, h):
    tensor = trans_to_dinov2(make(w, h))
    assert tuple(tensor.shape) == (3, 224, 224)
