#
# cd 2024_tokyo/vote_on_the_day/okutama
# python make_csv.py
#
import re
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_okutama.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
本文へ

奥多摩町 Okutama Town

文字サイズ
標準（初期状態）
拡大する
背景色変更
背景色を黒色にする
背景色を青色にする
背景色を元に戻す
Foreign Language
各課のご案内

検索ファイル種別

すべて

HTML

PDF
くらし・手続き
健康・福祉・介護
子育て・教育
文化・観光
・スポーツ
しごと・産業
町政情報
現在のページ
ホーム 行政情報サイト 町政情報 選挙 投票所について
あしあと
選挙投票所について選挙選挙投票所についてあしあとを消去する
投票所について


更新日：2022年06月24日
投票所及び投票場所等
 

投票所一覧
投票所	投票場所	自治会




この記事に関するお問い合わせ先
総務課 庶務係

奥多摩町氷川215-6

電話番号：0428-83-2345
ファクス：0428-83-2344

お問い合わせはこちら
みなさまのご意見をお聞かせください
このページの内容は分かりやすかったですか
わかりやすかった普通わかりにくかった
このページは見つけやすかったですか
見つけやすかった普通見つかりにくかった
選挙
奥多摩町長選挙開票結果
奥多摩町長選挙投票結果
奥多摩町長選挙選挙公報
奥多摩町長選挙告示・立候補届
投票について
投票所について
選挙権と被選挙権
在外選挙
寄付の禁止
選挙結果
ページトップへ
東京都 奥多摩町役場

〒198-0212 東京都西多摩郡奥多摩町氷川215-6

電話：0428-83-2111（代表）

お問い合わせ
交通アクセス
サイトマップ
庁舎案内
アクセシビリティ
プライバシーポリシー
リンク集
Copyright (c) 2022 Okutama Town. All Rights Reserved.
"""

# 除外行のリスト
except_lines = []

for line in except_lines_as_text.split("\n"):
    line = line.strip()
    # 空行は除外
    if line != '':
        except_lines.append(line)


def is_ignore_line(line):
    """この行を無視するか？"""

    # 空行
    if line == '':
        return True

    return line in except_lines


def double_quote(text):
    """カンマが含まれていれば、二重引用符で囲む"""
    if ',' in text:
        return f'"{text}"'

    return text


def to_formatted_header_string():
    """出力テキスト形式のヘッダー"""
    return f'投票区番号,住所,施設名'


def to_formatted_data_record_string(
        ward_number,
        address,
        name_of_facility):
    """出力テキスト形式のデータ"""
    address_2 = f'{address} {name_of_facility}'
    return f'''{ward_number},{double_quote(address_2)},{double_quote(name_of_facility)}'''


########################################
# 人間の目視確認によるデータの手調整
########################################

def processing_data():
    pass


########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    print(f'[{datetime.datetime.now()}]  read `{input_file_name}` file...')

    with open(input_file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()


    # 見出し
    ward_number = None
    name_of_facility = None
    address = None

    output_table = []

    # 出力フォーマット
    output_table.append(to_formatted_header_string())

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[{datetime.datetime.now()}]  [read line] {line}")

        # ［投票区の番号］、［施設名］を判断。［住所］は書いてない
        #
        #   例： `第1投票所	川井生活館	川井・梅沢`
        #
        m = re.match(r'^第(\d+)投票所\t(\S*)(\t.*)?', line)
        if m:
            ward_number = int(m.group(1))
            name_of_facility = m.group(2)
            address = '東京都西多摩郡奥多摩町'

            #print(f"[{datetime.datetime.now()}]    [parse]  投票区の番号：{ward_number}  施設名：{name_of_facility}")

            #
            # flush
            #
            # 出力フォーマット
            output_line = to_formatted_data_record_string(
                    ward_number=ward_number,
                    address=address,
                    name_of_facility=name_of_facility)
            #print(f"[{datetime.datetime.now()}]    [出力]  {output_line}")
            output_table.append(output_line)

            continue


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')


    #
    # 以下、データ内容に加工が必要なものは、調整します
    #
    processing_data()

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
