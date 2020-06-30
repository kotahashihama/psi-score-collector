## PageSpeed Insights 一括採点スクリプト

### 導入手順

1. `psi-score-collector` をクローンする
2. Python 3.8 以上をインストールする
3. Poetry のインストール
4. 仮想環境の作成とライブラリのインストール
5. API キーのセット
6. PSI 測定の実行

```
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

以後、クローンしてきた `psi-score-collector` ディレクトリ内で行う


### 仮想環境の作成とライブラリのインストール

完了後、 `.venv` ディレクトリができます

```
poetry config virtualenvs.in-project true
poetry install
```


### API キーのセット

以下コマンドを実行のうえで [PageSpeed Insight API](https://developers.google.com/speed/docs/insights/v5/get-started?hl=ja) より取得した API キーを `.env` の環境変数 `API_KEY` にセットする

```
cp .env .env.example
```


### PSI 測定の実行

`main.py` の変数 `url_list` へ測定する URL をセットする

```
poetry run python main.py
```
