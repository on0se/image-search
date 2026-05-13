from PIL import Image # 画像の読み込み、保存、リサイズ
import torchvision.transforms as T # 画像のリサイズ、正規化 Tはクラスが無数に入っているモジュール


def pad_to_square(img):
    """
    黒で埋めて画像を正方形にする
    引数:Imageクラス
    別の策：拡大して中心切り出しでもいいかもしれない
    """
    w, h = img.size
    max_siz = max(w, h)

    # 長い辺で黒の正方形を作り、中心に画像を貼る(座標指定は左上)
    new_img = Image.new("RGB", (max_siz, max_siz), (0, 0, 0))
    paste_x = (max_siz - w) // 2
    paste_y = (max_siz - h) // 2
    new_img.paste(img, (paste_x, paste_y))
 
    return new_img

def trans_to_dinov2(img):
    """
    DINOv2に画像を渡す前の前処理をする
    引数:Imageクラス
    パディング → 224 * 224にリサイズ → テンソル変換 → 正規化 の順に処理
    """
    # Resize、ToTensor等はクラス
    img = pad_to_square(img)
    img = T.Resize((224, 224))(img) 
    img = T.ToTensor()(img) # ImageからTensorへ変換
    img = T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])(img) # ImageNetの平均と標準偏差で正規化
    return img
