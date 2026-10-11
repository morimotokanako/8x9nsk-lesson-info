# 8x9nsk-lesson-info

ハック西宮北口校のレッスン用リンクページです。教室のPCのブラウザ起動ページ・ホームページに設定し、教材やツールへのアクセスを一か所にまとめます。

- [テスト公開ページ](https://morimotokanako.github.io/8x9nsk-lesson-info/)
- [GitHubリポジトリ](https://github.com/morimotokanako/8x9nsk-lesson-info)
- [作業ログ](./log.md)

## 目的

- 生徒が必要な教材へ迷わずアクセスできるようにする。
- リンクの変更をページ側に集約し、各PCのブックマークを個別に修正する手間を減らす。
- Gitのコミット履歴で変更を管理し、GitHubへのpushを公開ページへ自動反映する。

## ページ仕様

- 主な利用環境：教室のPCブラウザ。
- 見出し：今日も楽しくプログラミングしよう！
- リード文：レッスンが始まったらハックベースにアクセスしましょう。
- デザイン：全幅の淡いグリーン系背景に、角丸のカード型ボタンを中央配置。
- メイン教材は3列、サブ教材は4列を基本とし、狭い画面では折り返す。
- 教材リンクは新しいタブで開く。
- HTMLとCSSを別ファイルで管理する静的ページ。ビルドやパッケージのインストールは不要。
- アイコンには絵文字を使用。見た目はOSやブラウザによって異なる。

## 掲載リンク

### メイン（左から順）

| ボタン | リンク先 |
| --- | --- |
| typing.com | [生徒ログイン](https://www.typing.com/student/login) |
| ハックベース | [レッスン入口](https://8x9base.com/lesson-entry) |
| ハックチャット | [ログイン](https://dev-8x9-ai.whole.jp/login) |

### サブ（左から順）

| ボタン | リンク先 |
| --- | --- |
| ichigojam web | [IchigoJam web](https://fukuno.jig.jp/app/IchigoJam/) |
| microbit makecode | [MakeCode](https://makecode.microbit.org/?lang=ja) |
| firealpaca | [ダウンロード](https://firealpaca.com/ja/download/) |
| マイクライベント案内 | [イベント詳細](https://em.8x9.jp/events/18) |

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `index.html` | 見出し、説明文、教材リンク、ボタンの並び順 |
| `style.css` | 色、余白、文字サイズ、カード配置、画面幅への対応 |
| `README.md` | 概要、仕様、運用手順 |
| `log.md` | 作業内容・確認結果の記録（小文字のファイル名） |
| `.gitignore` | Git管理から除外するファイル・フォルダの指定 |

`outputs/`（バックアップ）、`work/`（一時作業）、`.DS_Store`はGit管理対象外です。

## 公開設定

- 公開サービス：GitHub Pages。
- 既定ブランチ：`main`。
- Settings → Pages → Source：`Deploy from a branch`。
- 公開元：`main` / `/ (root)`。
- `main`へpushすると公開処理が始まる。反映完了まで少し時間がかかる場合がある。
- 教室PCには、上記のテスト公開ページのURLを起動ページ・ホームページとして設定する。

## 作業ログの記入ルール

- `log.md`へ日付・変更内容・確認結果を簡潔に記載する。
- 新しい記録を上に追加する。同日の記録も新しい順に並べる。
- 検証内容は対象の作業記録に添え、確認済み・未確認を区別する。
- バージョン管理はGitのコミット履歴を使用する。
- READMEと作業ログも公開リポジトリで共有されるため、パスワードなどの認証情報は記載しない。

## 編集・公開の手順

1. VS Codeでこのリポジトリのフォルダを開く。
2. ターミナルで`git status`を確認し、未コミットの変更がない状態で`git pull --ff-only origin main`を実行して最新版を取得する。
3. 文言・リンク・並び順は`index.html`、デザインは`style.css`を編集する。
4. ローカルの`index.html`をブラウザで開き、表示とリンク先を確認する。
5. `log.md`の先頭へ作業記録を追加する。概要や仕様が変わる場合は`README.md`も更新する。
6. 変更内容を確認してコミットし、GitHubへpushする。
7. GitHubのActionsで公開処理の成功を確認し、公開ページを再読み込みして反映を確認する。

### ターミナル記述例

リポジトリのフォルダ内で実行します。

```bash
git status
git diff
git add index.html style.css README.md log.md
git diff --cached
git commit -m "教材リンクと作業ログを更新"
git push origin main
```

- `git add`：変更したファイルをコミット対象にする。
- `git diff --cached`：コミット対象の変更内容を確認する。
- `git commit`：変更内容に説明を付けてローカルの履歴に保存する。
- `git push origin main`：コミットをGitHubへ送り、Pagesの公開更新を開始する。

VS Codeのソース管理から、変更のステージ・コミット・pushを行うこともできます。
