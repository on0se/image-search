from fastapi import FastAPI, UploadFile, File, Depends
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

# データベース
class ImageDB:
    def __init__(self):
        self.vectors = [] # 画像ベクトルのリスト
        self.index = None # faissインデックス

image_db = ImageDB()

def get_db():
    return image_db

@app.post("/upload")
async def upload(
    files: List[UploadFile] = File(...),
    db: ImageDB = Depends(get_db) # Dependency Injection
):
    """
    写真をデータベースにアップロードする
    引数: アップロードする写真
    処理: 写真ベクトルリスト、faissインデクスの更新
    返り値: アップロードした画像の枚数
    """
    add_count = 0
    
    for file in files:
        content = await file.read()
        vector = vectorize_image(Image.open(io.BytesIO(content)).convert("RGB"))
        db.vectors.append(vector)
        db.index = add_index(vector.reshape(1, -1), db.index)
        add_count += 1
    
    return {"count": add_count}

@app.post("/search")
async def search(
    topK: int = 1,
    file: UploadFile = File(...),
    db: ImageDB = Depends(get_db) # Dependency Injection
):
    """
    クエリ写真に似た写真を検索する
    引数: クエリ写真
    処理: 似た写真をfaissで検索する
    返り値: 似た写真の写真データベース上の添え字
    """
    topK = min(topK, len(db.vectors))
    content = await file.read()
    vector = vectorize_image(Image.open(io.BytesIO(content)).convert("RGB"))
    results = faiss_search(db.index, vector, topK)
    return {"results": results}