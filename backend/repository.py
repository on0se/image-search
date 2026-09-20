import abc

from searcher import add_index, faiss_search

# データベース(抽象的)
class ImageRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, vector) -> None:
        """ベクトルを1つ追加"""
        pass
    
    @abc.abstractmethod
    def search(self, query_vector, topk) -> list:
        """クエリベクトルに近い画像をtopk件検索し、添え字リストを返す"""
        pass

    @abc.abstractmethod
    def count(self) -> int:
        """登録済みの画像数を返す"""
        pass

# メモリで管理するデータベース
class InMemoryImageRepository(ImageRepository):
    def __init__(self):
        self.index = None # faissインデックス
    
    def add(self, vector) -> None:
        self.index = add_index(vector.reshape(1, -1), self.index)
    
    def search(self, query_vector, topk) -> list:
        return faiss_search(self.index, query_vector, topk)

    def count(self) -> int:
        if self.index is None:
            return 0
        return self.index.ntotal
