set -e

# 基本となるindexを作成する
python 701_create_index.py

# index_riverを作成する
python 301_update_index.py

# index_bookを作成する
# ここで、app_dirのitem以下のファイルを更新する。
python 500_book.py

# 「水名」と「水経注：巻」を含むcurationを作成する
python 600_update_curation.py

# アノテーション付きのlayer画像を作成する。
# 出力ファイル: docs/iiif/*/manifest_anno.json
python 800_annotations.py