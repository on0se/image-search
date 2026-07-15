import os
import json
import faiss

from searcher import add_index, faiss_search

class ImageIndex:
    """
    ベクトル検索用インデックス。
    FAISSは検索処理自体がメモリ上の構造を前提とするため、
    「保存先を切り替え可能にする」というRepositoryパターンの
    恩恵を実質的に得られない。そのため抽象クラスにはせず、
    素直な実装にとどめている。
    保存先はディスク決め打ちとする。
    """
    def __init__(self, index_path: str, names_path: str):
        self.index_path = index_path
        self.names_path = names_path
        self.index = None
        self.filenames = []
        self.filename_set = set()
        self.load()

    def add(self, vector, filename: str) -> bool:
        if filename in self.filename_set:
            return False
        self.index = add_index(vector.reshape(1, -1), self.index)
        self.filenames.append(filename)
        self.filename_set.add(filename)
        return True
    
    def search(self, query_vector, topk) -> list:
        if self.index is None:
            return []
        indices = faiss_search(self.index, query_vector, topk)
        return [self.filenames[i] for i in indices]

    def count(self) -> int:
        return 0 if self.index is None else self.index.ntotal
    
    def list_filenames(self) -> list:
        return self.filenames
    
    def save(self) -> None:
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
        with open(self.names_path, "w") as f:
            json.dump(self.filenames, f)
    
    def load(self) -> None:
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
        if os.path.exists(self.names_path):
            with open(self.names_path) as f:
                self.filenames = json.load(f)
                self.filename_set = set(self.filenames)