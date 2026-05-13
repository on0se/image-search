import streamlit as st
from PIL import Image
from vectorizer import vectorize_image
from searcher import search, add_index
import numpy as np
import faiss
from pathlib import Path
import json

st.title("似た画像検索")

# 画像データベースのディレクトリ作成
Path("db_imgs").mkdir(exist_ok=True) 

# データベースと索引構造はセッションをまたいで管理する
if "imgs" not in st.session_state:
    # 以前にデータベースを作成済みの場合はそれを用いる
    if Path("index.faiss").exists():
        st.session_state.index = faiss.read_index("index.faiss")
        st.session_state.img_vectors = list(np.load("vectors.npy"))
        with open("uploaded_names.json", "r") as f:
            st.session_state.uploaded_names_order = json.load(f)
        st.session_state.uploaded_names = set(st.session_state.uploaded_names_order)  # setはorderから作る
        st.session_state.imgs = [Image.open(f"db_imgs/{name}").convert("RGB") for name in st.session_state.uploaded_names_order]  # 順番通りに読み込む

    else:
        st.session_state.imgs = [] # 画像リスト
        st.session_state.img_vectors = [] # 画像ベクトルリスト
        st.session_state.index = None # faiss索引構造
        st.session_state.uploaded_names_order = [] # アップロードした画像の順番を管理
        st.session_state.uploaded_names = set() # アップロードした名前の管理


# 1. 画像データベースアップロードとインデックス構築
uploaded_files = st.file_uploader("画像をアップロード", type = ["jpg", "png"], accept_multiple_files=True)
index_button = st.button("画像データベースを更新") # ボタンを押すときのみ更新する(uploaded filesはセッション間で保持されるためこれで管理できない)

# アップロードされた画像の追加、ベクトル化、索引構造の更新
if index_button and uploaded_files:
    for file in uploaded_files:
        if file.name not in st.session_state.uploaded_names: # まだ追加していない画像を追加
            img = Image.open(file).convert("RGB")
            img_vec = vectorize_image(img)
            # 名前の管理
            st.session_state.uploaded_names.add(file.name)
            st.session_state.uploaded_names_order.append(file.name)
            # 画像データの管理
            st.session_state.imgs.append(img)
            img.save(f"db_imgs/{file.name}") # 差分のみ更新(一括は重いので)
            # 画像ベクトルの管理
            st.session_state.img_vectors.append(img_vec)
            # 索引構造の管理
            st.session_state.index = add_index(img_vec.reshape(1, -1), st.session_state.index) # (要素数, vec)の形で渡す

    # ローカルに一括保存 : 名前、画像ベクトル、索引構造
    with open("uploaded_names.json", "w") as f:
        json.dump(st.session_state.uploaded_names_order, f)
    np.save("vectors.npy", np.stack(st.session_state.img_vectors))
    faiss.write_index(st.session_state.index, "index.faiss")
    

# 2. 検索画像のアップロード
uploaded_file = st.file_uploader("検索画像", type = ["jpg", "png"])
query_img = None
query_vec = None
if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    query_img = img
    query_vec = vectorize_image(img)

st.sidebar.title("設定")
top_k = st.sidebar.slider("表示数", min_value = 1, max_value = 20, value = 10) # TopKの値の設定

# 3. 画像検索
if st.session_state.index is not None and query_vec is not None:
    results = search(st.session_state.index, query_vec, st.session_state.imgs, top_k)

    # 幅4のグリッドで出力
    wid = 4
    for i in range(0, len(results), wid):
        cols = st.columns(wid) # 行を作る
        for col, img in zip(cols, results[i : i + wid]):
            with col:
                st.image(img, use_container_width = True)        