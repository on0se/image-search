"""
pytest の設定ファイル。

中身は空でよく、このファイルが backend/ に存在すること自体に意味がある。
pytest は conftest.py を見つけると、そのディレクトリを import の検索パスに追加する。
これがないと backend/tests/ から `from preprocess import ...` が解決できない。

テスト全体で共有したいものができたら、ここへ置く。
"""
