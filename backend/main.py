from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import List

from vectorizer import vectorize_bytes
from repository import ImageRepository, InMemoryImageRepository

# サーバー起動時にRepositoryを作り、appに紐づける
@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.image_repo = InMemoryImageRepository()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_repo(request: Request) -> ImageRepository:
    return request.app.state.image_repo

@app.post("/upload")
async def upload(
    files: List[UploadFile] = File(...),
    repo: ImageRepository = Depends(get_repo)
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
        vector = vectorize_bytes(content)
        repo.add(vector)
        add_count += 1
    
    return {"count": add_count}

@app.post("/search")
async def search(
    topK: int = 1,
    file: UploadFile = File(...),
    repo: ImageRepository = Depends(get_repo)
):
    """
    クエリ写真に似た写真を検索する
    引数: クエリ写真
    処理: 似た写真をfaissで検索する
    返り値: 似た写真の写真データベース上の添え字
    """
    topK = min(topK, repo.count())
    content = await file.read()
    vector = vectorize_bytes(content)
    results = repo.search(vector, topK)
    return {"results": results}