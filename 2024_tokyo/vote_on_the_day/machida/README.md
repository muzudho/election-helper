# ［東京都選挙管理委員会　＞　（当日の）投票所一覧　＞　町田市　Ｗｅｂページ］の投票所一覧をＣＳＶに変換するＰｙｔｈｏｎスクリプト


# 入力データ

![東京都選挙管理委員会　＞　（当日の）投票所一覧　＞　町田市　Ｗｅｂページ](./res/202406__senkyo__28-2118-vote-on-the-day-machida-input-web.png)  

* 📖 [東京都選挙管理委員会事務局　＞　都内区市町村選管等問い合わせ先](https://www.senkyo.metro.tokyo.lg.jp/kushichoson-contact/)
  * 地図内： 町田市　から　📖 [東京都選挙管理委員会　＞　（当日の）投票所一覧　＞　町田市　Ｗｅｂページ](https://www.city.machida.tokyo.jp/shisei/senkyo/tohyo/20121001touhyoujoitiran.html)  

👆　リンクをクリックして、開いたＷｅｂページで `[Ctrl] + [A]` キーを押すなどして全文選択して `[Ctrl] + [C]` キーを押すなどしてコピー  

![input_data.txt](./res/202406__senkyo__28-2121-vote-on-the-day-machida-input-text.png)  

👆　📄 `input_data.txt` という名前のテキストファイルへその内容を貼り付け


## ＣＳＶ変換の実行

![ターミナル](./res/202406__senkyo__28-2136-vote-on-the-day-machida-terminal.png)  

例えば以下の通り  

```shell
cd 2024_tokyo/vote_on_the_day/machida
python make_csv.py
```


## 出力データ

![output_data_machida.csv](./res/202406__senkyo__28-2138-vote-on-the-day-machida-output-text.png)  

👆　📄 `output_data_machida.csv` 参照


## グーグルマップへのインポート

別サイトの記事を参考にしてください  

* 📖 [住所のCSVファイルをインポートする](https://diamond.jp/articles/-/308329?page=2)  
