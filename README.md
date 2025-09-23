# YGO Genesys Deck Builder / 游戏王分数制组卡器 / 遊戯王ジェネシス デッキビルダー

[English](#english) | [中文 (Chinese)](#中文-chinese) | [日本語 (Japanese)](#日本語-japanese)

---

## English

A desktop application for the "Yu-Gi-Oh! Genesys" constructed format. This tool helps players build regulation-compliant decks using the official point system.

### Features
* **Deck Management**: Create, open, and save YGOPro-compatible `.ydk` files.
* **Card Search**: Quickly search cards by name with multi-language support.
* **Detailed View**: View card images, descriptions, types, and point costs.
* **Intuitive Interface**: Add cards via double-click or buttons, with real-time stat tracking.
* **Multi-language Support**: Switch between English, Chinese, and Japanese.

### Requirements
* Python 3
* PySide6
* `pics` folder with card images (Optional)

### Installation
1.  Install dependencies:
    ```bash
    pip install PySide6
    ```
2.  (Optional) Create a `pics` folder. Download card images and name them `{card_ID}.jpg`.

### Usage
1.  Run the script: `python YGOgenesys_deck_builder.py`
2.  Use the search bar to find cards.
3.  Single-click a card to view details. Double-click to add it to your deck or remove it.
4.  Use the "File" menu to manage your deck files.

### Data Sources
* **Card Data**: `https://ygocdb.com/`
* **Point Costs & Rules**: `https://www.yugioh-card.com/en/genesys/`

### License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 中文 (Chinese)

一款“游戏王 Genesys”构筑赛桌面应用，帮助玩家基于官方分数系统，构建符合规则的卡组。

### 功能
* **卡组管理**: 新建、打开和保存 YGOPro 兼容的 `.ydk` 文件。
* **卡片检索**: 按卡名快速搜索，支持多语言显示。
* **详细信息**: 查看卡图、描述、种类和分数成本。
* **直观界面**: 通过双击或按钮添加卡片，实时追踪卡组数据。
* **多语言支持**: 可随时切换中、日、英文界面。

### 运行要求
* Python 3
* PySide6
* `pics` 文件夹，存放卡片图片（可选）

### 安装
1.  安装依赖:
    ```bash
    pip install PySide6
    ```
2.  (可选) 创建 `pics` 文件夹，下载卡图并命名为 `{卡片ID}.jpg`。

### 使用说明
1.  运行脚本: `python YGOgenesys_deck_builder.py`
2.  使用搜索框查找卡片。
3.  单击卡片查看详情，双击可将其添加至卡组或者删除。
4.  使用“文件”菜单管理卡组文件。

### 数据来源
* **卡片数据**: `https://ygocdb.com/`
* **分数成本与规则**: `https://www.yugioh-card.com/en/genesys/`

### 许可
本项目采用 MIT 许可协议。详情请见 [LICENSE](LICENSE) 文件。

---

## 日本語 (Japanese)

「遊戯王ジェネシス」構築戦用のデスクトップアプリです。公式ポイントシステムに基づき、プレイヤーがルールに適合したデッキを構築するのを支援します。

### 機能
* **デッキ管理**: YGOPro互換の`.ydk`ファイルの新規作成、開封、保存。
* **カード検索**: カード名での迅速な検索、多言語表示に対応。
* **詳細情報**: カード画像、詳細、種類、ポイントコストの表示。
* **直感的なUI**: ダブルクリックまたはボタンでカードを追加、デッキデータをリアルタイムで追跡。
* **多言語サポート**: 日本語、中国語、英語のインターフェース切り替えが可能。

### 動作要件
* Python 3
* PySide6
* `pics` フォルダにカード画像を格納（任意）

### インストール
1.  依存ライブラリをインストール:
    ```bash
    pip install PySide6
    ```
2.  (任意) `pics` フォルダを作成し、カード画像を `{カードID}.jpg` 形式で保存。

### 使用方法
1.  スクリプトを実行: `python YGOgenesys_deck_builder.py`
2.  検索ボックスでカードを検索。
3.  カードをシングルクリックで詳細表示、ダブルクリックでデッキに追加または削除。
4.  「ファイル」メニューでデッキファイルを管理。

### データソース
* **カードデータ**: `https://ygocdb.com/`
* **ポイントコストとルール**: `https://www.yugioh-card.com/en/genesys/`

### ライセンス
このプロジェクトはMITライセンスです。詳細は [LICENSE](LICENSE) ファイルをご覧ください。