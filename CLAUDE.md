# Python Scripts - UV スクリプトモード対応リポジトリ

## 概要

このリポジトリは、[uv](https://github.com/astral-sh/uv)のスクリプトモードで実行できるスタンドアローンのPythonスクリプトを集めたものです。各スクリプトは依存関係の情報を含んでおり、uvが自動的に必要なパッケージをインストールして実行します。

## uvとは

uvは、Rustで書かれた超高速なPythonパッケージマネージャーおよびプロジェクト管理ツールです。pipやvenvの代替として使用でき、依存関係の解決とインストールが非常に高速です。

## uvスクリプトモードとは

uvのスクリプトモード（PEP 723準拠）では、Pythonスクリプトファイルの先頭に依存関係情報を記述することで、スタンドアローンで実行可能なスクリプトを作成できます。

### スクリプトの形式

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "pandas",
# ]
# ///

import numpy as np
import pandas as pd

# スクリプトの本体
```

この形式により、以下の利点があります：
- 仮想環境の手動作成が不要
- 依存関係が自己文書化される
- スクリプト単体で配布・共有が容易

## スクリプト一覧

### 1. tcp-echo-server.py

TCPエコーサーバーの実装です。クライアントから受信したデータをそのまま返送します。

**依存関係**: なし（標準ライブラリのみ）

**使い方**:
```bash
uv run tcp-echo-server.py 12345
```

**機能**:
- 指定されたポートでTCPサーバーを起動
- クライアントからの接続を受け付ける
- 受信したデータをエコーバック

### 2. multiprocess-sample.py

Pythonのマルチプロセス処理とソケット通信を組み合わせたデモスクリプトです。

**依存関係**:
- numpy
- colorama（ターミナル出力の色付け）
- matplotlib（実行時間の可視化）

**使い方**:
```bash
# 先にエコーサーバーを起動
uv run tcp-echo-server.py 12345

# 別のターミナルでクライアントを実行
uv run multiprocess-sample.py
```

**機能**:
- マルチプロセスプールを使用して複数のタスクを並行実行
- 各タスクがTCPエコーサーバーと通信
- ロックを使用したプロセス間の同期
- coloramaによるカラフルな出力
- matplotlibによるタスク実行時間の可視化

## uvのインストール

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# pipでのインストール
pip install uv
```

## 実行方法

uvがインストールされていれば、各スクリプトは以下のコマンドで実行できます：

```bash
uv run <スクリプト名.py> [引数]
```

uvは自動的に：
1. スクリプトのメタデータを読み取る
2. 必要な依存関係を解決
3. 一時的な仮想環境を作成
4. 依存関係をインストール
5. スクリプトを実行

## スクリプトの追加方法

新しいスクリプトを追加する場合は、以下の形式でファイルの先頭にメタデータを記述してください：

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "パッケージ名1",
#   "パッケージ名2>=バージョン",
# ]
# ///

# ここからスクリプトの本体
```

## コードフォーマット

このリポジトリでは、コード品質を保つために[ruff](https://github.com/astral-sh/ruff)を使用しています。ruffは、Rust製の超高速なPythonリンター＆フォーマッターです。

### ruffの特徴

- **高速**: Rustで書かれており、従来のツールより10〜100倍高速
- **オールインワン**: フォーマット＋リント機能を統合
- **設定不要**: デフォルトで適切な設定が動作
- **uvと同じAstral製**: uvとの相性が良い

### コードのフォーマット

```bash
# すべてのPythonファイルをフォーマット
uvx ruff format .

# 特定のファイルをフォーマット
uvx ruff format script.py
```

### コードのリント（静的解析）

```bash
# すべてのPythonファイルをチェック
uvx ruff check .

# 自動修正可能な問題を修正
uvx ruff check --fix .

# 特定のファイルをチェック
uvx ruff check script.py
```

### pre-commitフックの使用

コミット前に自動的にruffを実行するには、pre-commitフックを設定します：

```bash
# pre-commitのインストール
uvx pre-commit install

# 手動で実行
uvx pre-commit run --all-files
```

これにより、git commitを実行する際に自動的にコードがフォーマット・チェックされます。

### 設定ファイル

ruffの設定は`pyproject.toml`に記述されています。主な設定：

- **行の長さ**: 88文字（Black互換）
- **Pythonバージョン**: 3.11以上
- **有効なルール**: pycodestyle、pyflakes、isort、pep8-naming、pyupgrade等

## 参考リンク

- [uv公式ドキュメント](https://docs.astral.sh/uv/)
- [PEP 723 - Inline script metadata](https://peps.python.org/pep-0723/)
- [uvスクリプトモードのドキュメント](https://docs.astral.sh/uv/guides/scripts/)
- [ruff公式ドキュメント](https://docs.astral.sh/ruff/)
