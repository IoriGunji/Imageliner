# Image Liner

画像に枠線をつけるアプリケーションです。

## 環境構築

パッケージのインストール

### pyproject.toml の修正

pyproject.toml を下記のように修正

```diff
[tool.poetry.dependencies]
- python = "^3.11"
+ python = "^3.11,<3.13"
```

### pip の場合

```shell
pip install pillow
pip install webcolors
pip install tkinterdnd2
pip install pyinstaller
```

### Poetry の場合

```shell
poetry add pillow
poetry add webcolors
poetry add tkinterdnd2
poetry add pyinstaller
```

## PyInstaller

PyInstaller の実行手順は下記のとおりです。

### hook-tkinterdnd2.py のダウンロード

PyInstaller を利用する場合、 hook-tkinterdnd2.py が必要になります。
Github からダウンロードして利用してください。

https://github.com/pmgagne/tkinterdnd2

`hook-tkinterdnd2.py` をスクリプトと同一のディレクトリに保存します。

### PyInstaller の実行

PyInstaller で実行ファイルを作成する場合は、次のオプションを追加します。

```shell
--additional-hooks-dir .
```

例

```shell
poetry run pyinstaller ./imageliner/gui.py --name ImageLiner --onefile --noconsole --icon=./imageliner/icon.ico --collect-data tkinterdnd2 --additional-hooks-dir ./imageliner
```
