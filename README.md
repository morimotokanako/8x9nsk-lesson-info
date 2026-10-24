# 8x9nsk-lesson-info

ハック西宮北口校のレッスン用リンクページです。教室のPCのブラウザ起動ページ・ホームページに設定し、教材やツールへのアクセスを一か所にまとめます。

- [テスト公開ページ](https://morimotokanako.github.io/8x9nsk-lesson-info/)
- [GitHubリポジトリ](https://github.com/morimotokanako/8x9nsk-lesson-info)
- [作業ログ](./log.md)
- [予定の管理・更新](https://morimotokanako.github.io/8x9nsk-lesson-info/admin.html)

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
- PCの表示領域1280×650・1366×650を目安に、高さに応じて余白とカードを縮小。拡大表示や予定が多い場合はスクロールできる。
- 教材リンクは新しいタブで開く。
- HTML・CSS・予定表示用JavaScriptを分離。APIの取得はGitHub ActionsのPython処理で行う。
- ハックベースには公式キャラクター、左上のヘッダーには公式ロゴを使用。その他のアイコンは絵文字で、OSやブラウザによって見た目が異なる。

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
| 8x9上級コース | [上級コース教材](https://8x9.notion.site/8x9-9d2c09c50df047fd9d2779629bd6be53?pvs=143) |
| ピクトグラミング | [ピクトグラミング](https://pictogramming.org/toppage/) |
| firealpaca | [ダウンロード](https://firealpaca.com/ja/download/) |
| NASサーバー | [ファイル保存](https://iot.myasustor.com:8801/portal/?6ADC2DCA) |

## ファイル構成

| ファイル | 役割 |
| --- | --- |
| `index.html` | 見出し、説明文、教材リンク、ボタンの並び順 |
| `style.css` | 色、余白、文字サイズ、カード配置、画面幅への対応 |
| `README.md` | 概要、仕様、運用手順 |
| `log.md` | 作業内容・確認結果の記録（小文字のファイル名） |
| `.gitignore` | Git管理から除外するファイル・フォルダの指定 |
| `lessons.js` | 開催中・次回の予定表示、有効期限・取得失敗の表示 |
| `admin.html` / `admin.css` | GitHubの設定・手動更新画面への案内 |
| `scripts/fetch_lessons.py` | APIの全件取得・検証・公開用JSON生成 |
| `.github/workflows/pages.yml` | 検証・取得・Pagesへの公開 |
| `data/lessons.json` | 未設定時の初期表示用データ（実データは公開処理時に生成） |
| `tests/` | 取得データ・表示判定の模擬検証 |

`outputs/`（バックアップ）、`work/`（一時作業）、`.DS_Store`はGit管理対象外です。

## 公開設定

- 公開サービス：GitHub Pages。
- 既定ブランチ：`main`。
- Settings → Pages → Source：`GitHub Actions`。
- 公開元：`main`のワークフローで生成する`public/`。
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
4. ローカルでは`python3 -m http.server 8000 --bind 127.0.0.1`を実行し、`http://127.0.0.1:8000/`で表示を確認する。ファイルを直接開く方法では予定JSONを読み込めない場合がある。
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

## API連携の叩き台

WordPressは使用しません。オンラインでの設定・実行にはGitHubの認証と権限管理を使用します。`admin.html`は公開の案内ページであり、キーを入力・保存する画面はGitHub側です。

1. Settings → Secrets and variables → Actions → Secretsで、`HACK_RESERVATION_API_TOKEN`を登録する。値は発行済みAPIキー本体。
2. Variablesで`LESSON_CLASSROOM_IDS`に対象教室IDをカンマ区切りで登録する。教室IDは予約システムと照合する。
3. 日時・コース名・教室名を一般公開してよいことを確認して、Variable `LESSON_API_ENABLED`を`true`にする。
4. Actions →「レッスン予定の取得・ページ公開」→ Run workflow（main）を実行する。
5. 成功後、公開ページの最終更新時刻と、実際の予定を照合する。

初期状態では実APIを呼ばず「予定は準備中」と表示します。LocalWPの保存済みキーは移していません。管理者が上記Secretsに登録してください。キーをチャット・HTML・Gitの履歴に記載しないでください。

- 当月・翌月を月単位で取得し、全教室・全ページの検証成功時だけ公開する。
- APIは既存と同じ固定のHTTPSエンドポイントへBearer認証でGETする。リダイレクトに追従しない。
- 下書きは除外。既存HP固有の体験コース除外は適用しない。同時刻の別レッスンも保持する。
- 開始時刻以上・終了時刻未満の予定は「レッスン中」として時刻・コース名を表示し、次回予定と併記する。30秒ごとに判定する。
- 講師の項目は未確定のため表示しない。生徒・予約情報・内部IDは公開JSONに含めない。
- 毎時45分（日本時間、24時間）に自動取得する。手動実行とmainへのpush時にも取得する。GitHub側の混雑で定期実行が遅延・スキップされる場合がある。公開リポジトリでは60日間活動がないと定期実行が無効になるため、その場合はActionsで再有効化する。
- 公開データの有効期限は取得開始から24時間。表示ページは5分ごとにJSONを読み直し、30秒ごとに開催中・次回を判定する。
- 正常0件は予定なしとして反映。取得・検証失敗時はワークフローを失敗終了し、公開中のサイトを保持する。期限切れの予定は表示しない。
- `LESSON_API_ENABLED`をfalseにして実行すると、公開予定を準備中表示に戻す。
- 実データはGitにコミットせずPages配布物に含める。公開ファイルはHTML・CSS・JS・表示用JSONだけ。
- スタッフの手動実行にはリポジトリへの書き込み権限が必要。Secretsの設定は管理者が担当する。

検証コマンド：`python3 -m unittest discover -s tests -v`、`node tests/lessons.test.cjs`。
