# ［東京都選挙管理委員会　＞　期日前投票所一覧　Ｗｅｂページ］の投票所一覧をＣＳＶに変換するＰｙｔｈｏｎスクリプト


## 入力データ

![東京都選挙管理委員会　＞　期日前投票所一覧　Ｗｅｂページ](./res/202406__senkyo__24-0013-webpage.png)  

📖 [東京都選挙管理委員会　＞　期日前投票所一覧　Ｗｅｂページ](https://r6tochijisen.metro.tokyo.lg.jp/vote/index.html)  

👆　リンクをクリックして、開いたＷｅｂページで `[Ctrl] + [A]` キーを押すなどして全文選択して `[Ctrl] + [C]` キーを押すなどしてコピー  

![input_data.txt](./res/202406__senkyo__24-0017-input-text.png)  

👆　📄 `input_data.txt` という名前のテキストファイルへその内容を貼り付け


## ＣＳＶ変換の実行

![ターミナル](./res/202406__senkyo__24-0016-terminal.png)  

例えば以下の通り  

```shell
cd 2024_tokyo/early_voting
python make_csv.py
```


## 出力データ

![output_data.txt](./res/202406__senkyo__24-0019-output-text.png)  

👆　📄 `output_data.txt` 参照

備考：グーグルマップが読み込めるCSVフォーマット  
📖 [地図上の対象物をファイルからインポートする](https://support.google.com/mymaps/answer/3024836?hl=ja&co=GENIE.Platform%3DDesktop)  

