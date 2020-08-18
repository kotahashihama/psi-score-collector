## PageSpeed Insights 一括採点スクリプト

### 導入手順

1. `psi-score-collector` をクローンする
1. Python 3.8 以上をインストールする
1. Poetry のインストール
1. 仮想環境の作成とライブラリのインストール
1. API キーのセット
1. PSI 測定の実行


### Poetry のインストール

```zsh
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

以後、クローンしてきた `psi-score-collector` ディレクトリ内で行う


### 仮想環境の作成とライブラリのインストール

完了後、 `.venv` ディレクトリが作成される

```zsh
poetry config virtualenvs.in-project true
poetry install
```


### API キーのセット

以下コマンドを実行のうえで [PageSpeed Insight API](https://developers.google.com/speed/docs/insights/v5/get-started?hl=ja) より取得した API キーを `.env` の環境変数 `API_KEY` にセットする

```zsh
cp .env .env.example
```


### PSI 測定の実行

`main.py` の

- 変数 `measurement_count` へ測定回数
- 変数 `url_list` へ測定する URL

をセットして以下を実行

```zsh
poetry run python main.py
```
