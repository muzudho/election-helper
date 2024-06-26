#
# cd 2024_tokyo/vote_on_the_day/hinode
# python make_csv.py
#
import re
import csv
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_hinode.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
ページの先頭です
共通メニューなどをスキップして本文へ

日の出町
ホームへ

language
読み上げ読み上げ設定
やさしい日本語
ふりがな
文字サイズ

標準
拡大
色の反転

標準
反転
〒190-0192東京都西多摩郡日の出町大字平井2780番地電話：042-597-0511（代表）


暮らし・手続き

子育て・教育

福祉・健康

事業者の方へ

町のとりくみ

施設

検索
日の出町へようこそ 観光・歴史・移住定住など

現在位置

ホーム町のとりくみ選挙・監査・会計選挙投票について
あしあと

選挙管理委員会（総務課庶務係内）投票区及び投票所
投票区及び投票所

町内の投票区及び投票所
　日の出町の投票区と投票所は、次のとおりです。




期日前投票所　　（町内の期日前投票所は1ヵ所です）
　　期日前投票所　　日の出町役場1階町民談話室　　平井2780番地

　　公（告）示日の翌日から、投票日の前日における期日前投票

お問い合わせ
東京都 日の出町　選挙管理委員会（総務課庶務係内）

電話: 042-588-4114

ファクス: 042-597-4369

電話番号のかけ間違いにご注意ください！

お問い合わせフォーム
この記事と同じ分類の記事
投票区及び投票所
選挙運動収支報告書
期日前投票
指定病院・老人ホーム等での不在者投票
代理投票
投票所入場整理券
滞在地での不在者投票
郵便等による不在者投票
選挙管理委員会（総務課庶務係内）
お知らせ
選挙について
選挙の記録
投票区及び投票所への別ルート
ホーム施設安全・安心・生活投票所
このサイトについてお問い合わせサイトマップアクセス
東京都 日の出町　

〒190-0192 東京都西多摩郡日の出町大字平井2780番地

電話：042-597-0511（代表） ファクス:042-597-4369 

役場開庁時間午前8時30分から午後5時15分(土曜・日曜・祝日・年末年始を除く)

法人番号：1000020133051

ページの先頭へ戻る
Copyright （C） Hinode Town All Rights Reserved.

共通メニューなどをスキップして本文へ


暮らし・手続き

子育て・教育

福祉・健康

事業者の方へ

町のとりくみ

施設
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
    print(f"[{datetime.datetime.now()}]  processing `{output_file_name}` file...")

    is_changed = False

    with open(output_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # 二次元配列
        row_list = [row for row in reader]
        for i in range(1, len(row_list)):
            row = row_list[i]

            #print(f'[{datetime.datetime.now()}]  [processing]  {row}')
            address = row[1]

            if address == '東京都西多摩郡日の出町平井1254番地1 日の出町立志茂町児童館':
                alternate = '東京都西多摩郡日の出町平井1254番地1 志茂町児童館'
                print(f"""\
[{datetime.datetime.now()}]  [processing]  住所加工。グーグル　マイマップでエラーになるから。「町立」が正しい所、グーグルマップの方は「立」が脱字？ 町名が２回出てくるのが検索に適さない？
    before: `{address}`
    after : `{alternate}`
""")
                row[1] = alternate
                is_changed = True


    # 変更があれば、再びファイル書出し
    if is_changed:
        print(f"[{datetime.datetime.now()}]  rewrite `{output_file_name}` file...")

        with open(output_file_name, 'w', encoding='utf-8') as f:
            for row in row_list:
                line = ','.join(row)
                #print(f"[{datetime.datetime.now()}]  [rewrite]  {line}")
                f.write(f'{line}\n')
    else:
        print(f"[{datetime.datetime.now()}]  no chagned")


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

        #print(f"[read   ] {line}")

        # ［投票区の番号］、［施設名］、［住所］か判断
        #
        #   例： `第1投票所　　日の出町立志茂町児童館　　平井1254番地1`
        #
        m = re.match(r'第(\d+)投票所　　(.*)　　(.*)', line)
        if m:
            ward_number = int(m.group(1))
            name_of_facility = m.group(2)
            address = f'東京都西多摩郡日の出町{m.group(3)}'


            # 出力フォーマット
            output_table.append(to_formatted_data_record_string(
                    ward_number=ward_number,
                    address=address,
                    name_of_facility=name_of_facility))


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
