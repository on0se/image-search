# image-search

画像をクエリにして、視覚的に似た画像を検索するアプリケーション。
DINOv2 で特徴量を抽出し、FAISS(HNSW) で近似最近傍探索する。

## デモ

![デモ](docs/demo.png)

クエリ画像を渡すと、登録済みの画像から似たものを返す。

## 技術スタック

- **バックエンド** — Python 3.11 / FastAPI / PyTorch (DINOv2) / FAISS
- **フロントエンド** — React 19 / Vite / Chakra UI

## セットアップ

バックエンド

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

フロントエンド（別のターミナル）

```bash
cd frontend
npm install
npm run dev
```

ブラウザで `http://localhost:5173/` を開く。

## 設計判断

埋め込みモデルの選定、前処理の方式、探索アルゴリズム、ベクトルDBを使わない判断については
[docs/design.md](docs/design.md) に記載しています。
