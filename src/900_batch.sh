set -e

# Omekaのコレクションからmanifestをダウンロードする
# python 900_download.py

# configで設定したラベルを名前とした持つフォルダを作成しつつ、layer機能を持つmanifestファイルを作成する。
python 901_merge.py

# manifestsフォルダ以下のIIIFマニフェストをdocsフォルダにコピーしつつ、IIIFコレクションを作成する
python 902_create_collection.py