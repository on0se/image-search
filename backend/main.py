from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from PIL import Image
import io

from vectorizer import vectorize_image
from searcher import add_index, faiss_search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# グローバル変数
db_vectors = [] # 画像ベクトルのリスト
index = None # faissインデックス
uploaded_names = set() # 画像の名前管理

@app.post("/upload")
async def upload(files: List[UploadFile] = File(...)):
    """
    写真をデータベースにアップロードする
    引数: アップロードする写真
    処理: 写真ベクトルリスト、faissインデクスの更新
    返り値: アップロードした画像の枚数
    """
    global db_vectors, index, uploaded_names
    add_count = 0
    
    for file in files:
        content = await file.read()
        name = file.filename
        if name not in uploaded_names:
            vector = vectorize_image(Image.open(io.BytesIO(content)).convert("RGB"))
            db_vectors.append(vector)
            index = add_index(vector.reshape(1, -1), index)
            uploaded_names.add(name)
            add_count += 1
    
    return {"count": add_count}

@app.post("/search")
async def search(topK: int = 10, file: UploadFile = File(...)):
    """
    クエリ写真に似た写真を検索する
    引数: クエリ写真
    処理: 似た写真をfaissで検索する
    返り値: 似た写真の写真データベース上の添え字
    """
    content = await file.read()
    vector = vectorize_image(Image.open(io.BytesIO(content)).convert("RGB"))
    results = faiss_search(index, vector, topK)
    return {"results": results}