# ゆにろぐ 🌰

## 動画・写真の追加
`media/` の中の、**フォルダの場所がそのままサイトの分類**になります。

- `media/land/show/ショー名/`
- `media/land/parade/パレード名/`
- `media/land/greeting/キャラ名/場所名/`
- `media/sea/ショー名/`

新しいショーは、フォルダを作って動画を入れるだけ。ファイル名は `20260315_01.mp4` のように日付を頭につけると、並び順がきれいです。
iPhoneの .mov は build.py が .mp4 に変換します(ffmpegが必要: `brew install ffmpeg`)。

## 更新手順
1. 動画を `media/...` に入れる
2. `python3 build.py`
3. `git add . && git commit -m "追加" && git push`

## 公開(自分だけが編集できる)
GitHubにリポジトリを作ってpushし、GitHub PagesかCloudflare Pagesで公開します。リポジトリに書き込めるのは自分だけなので、他の人は閲覧のみです。
- GitHub Pages: 1ファイル100MBまで、サイト全体1GB目安
- Cloudflare Pages: 1ファイル25MBまで → 動画が増えたら R2 に置き、index.html の `MEDIA_BASE` を R2のURLにする
