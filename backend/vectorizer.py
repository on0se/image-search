import torch
import numpy as np
from PIL import Image
from utils import trans_to_dinov2

# DINOv2モデルをロード
model = torch.hub.load("facebookresearch/dinov2", "dinov2_vitb14")
model.eval()  # 推論モード

def vectorize_image(img):
    """
    1枚のPIL画像をDINOv2に通してベクトルに変換する
    引数:Image
    返り値は shape (768,) のnumpy配列
    """
    # 前処理して (1, C, H, W) の形へ、PyTorchではバッチが必要(1枚ずつ処理)
    tensor = trans_to_dinov2(img).unsqueeze(0)

    # 変換する(推論のみなので学習用計算はしない)
    with torch.no_grad():
        vector = model(tensor)

    # numpy配列に変換して返す
    return vector.squeeze(0).numpy().astype("float32")