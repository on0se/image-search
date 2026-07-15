import abc
import os

class ImageRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, filename: str, content: bytes) -> None:
        """画像バイナリを保存する"""
        pass

    @abc.abstractmethod
    def get(self, filename: str) -> bytes:
        """画像バイナリを取得する"""
        pass
    
    @abc.abstractmethod
    def exists(self, filename: str) -> bool:
        """指定したファイルが存在するか確認する"""
        pass

class DiskImageRepository(ImageRepository):
    def __init__(self, save_dir: str):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def save(self, filename: str, content: bytes) -> None:
        path = os.path.join(self.save_dir, filename)
        with open(path, "wb") as f:
            f.write(content)
    
    def get(self, filename: str) -> bytes:
        path = os.path.join(self.save_dir, filename)
        with open(path, "rb") as f:
            return f.read()
    
    def exists(self, filename: str) -> bool:
        return os.path.exists(os.path.join(self.save_dir, filename))