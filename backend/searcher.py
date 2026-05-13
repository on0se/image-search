import faiss
import numpy as np

def add_index(vector, index):
    """
    FAISSのインデックスへベクトルを追加する
    """
    dim = vector.shape[1]          # ベクトルの次元数（DINOv2 vitb14は768次元）
    if index is None:
        index = faiss.IndexFlatL2(dim)
    index.add(vector)              # ベクトルをインデックスに登録
    return index

def search(index, query_vector, imgs, top_k=10):
    """
    クエリベクトルに最も近い画像をTop-K件検索する
    返り値は検索結果のリストで中身は画像
    """
    # FAISSはバッチ形式で受け取るので (1, 768) に変形する
    query = query_vector.reshape(1, -1).astype("float32")

    # 検索実行: distances=距離のリスト, indices=インデックス番号のリスト
    distances, indices = index.search(query, top_k)

    results = []
    for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
        results.append(imgs[idx])

    return results