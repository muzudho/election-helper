# ［東京都選挙管理委員会　＞　（当日の）投票所一覧　＞　瑞穂町　Ｗｅｂページ］の投票所一覧をＣＳＶに変換するＰｙｔｈｏｎスクリプト


# 入力データ

![東京都選挙管理委員会　＞　（当日の）投票所一覧　＞　瑞穂町　Ｗｅｂページ](./res/202406__senkyo__26-1951-vote-on-the-day-mizuho-input-web.png)  

* 📖 [東京都選挙管理委員会事務局　＞　都内区市町村選管等問い合わせ先](https://www.senkyo.metro.tokyo.lg.jp/kushichoson-contact/)
  * 地図内： 瑞穂町　から　📖 [東京都選挙管理委員会　＞　（当日の）投票所一覧　＞　瑞穂町　Ｗｅｂページ](https://www.town.mizuho.tokyo.jp/tyosei/020/001/p002802.html)  

👆　リンクをクリックして、開いたＷｅｂページで `[Ctrl] + [A]` キーを押すなどして全文選択して `[Ctrl] + [C]` キーを押すなどしてコピー  

![input_data.txt](./res/202406__senkyo__26-2012-vote-on-the-day-mizuho-input-text.png)  

👆　📄 `input_data.txt` という名前のテキストファイルへその内容を貼り付け


## ＣＳＶ変換の実行

![ターミナル](./res/202406__senkyo__26-2025-vote-on-the-day-mizuho-terminal.png)  

例えば以下の通り  

```shell
cd 2024_tokyo/vote_on_the_day/mizuho
python make_csv.py
```


## 出力データ

![output_data_mizuho.csv](./res/202406__senkyo__26-2026-vote-on-the-day-mizuho-output-text.png)  

👆　📄 `output_data_mizuho.csv` 参照


## グーグルマップへのインポート

別サイトの記事を参考にしてください  

* 📖 [住所のCSVファイルをインポートする](https://diamond.jp/articles/-/308329?page=2)  
