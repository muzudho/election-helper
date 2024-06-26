#
# cd 2024_tokyo/vote_on_the_day/akiruno
# python make_csv.py
#
import re
import csv
import datetime
import unicodedata
import pprint


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_akiruno.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
#
#   ※ PDF なので指定が難しい
#
except_lines_as_text = """\
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

        # 追加
        print(f'[{datetime.datetime.now()}]  [processing]  レコード追加。ＰＤＦ解析困難のため。')

        record = ['11', '名無し', '二宮３５０番地']
        pprint.pprint(record)
        row_list.append(record)
        is_changed = True

        record = ['13', '増戸小学校屋内運動場', '伊奈１１７３番地']
        pprint.pprint(record)
        row_list.append(record)

        record = ['14', '五日市ファインプラザ', '伊奈８５９番地３']
        pprint.pprint(record)
        row_list.append(record)

        record = ['16', '五日市小学校東裏校舎', '五日市３１５番地']
        pprint.pprint(record)
        row_list.append(record)

        pprint.pprint(row_list)


    # ［投票区の番号］順にソートしたい（二次元配列）
    print(f"[{datetime.datetime.now()}]  sort by 投票区の番号")

    # ヘッダー以外をソート
    row_list = sorted(row_list[1:],
            key=lambda row: int(row[0]))

    # ヘッダーを先頭に付ける
    row_list.insert(0, row_list[0])
    pprint.pprint(row_list)


    # 変更があれば、再びファイル書出し
    if is_changed:
        print(f"[{datetime.datetime.now()}]  rewrite `{output_file_name}` file...")

        with open(output_file_name, 'w', encoding='utf-8') as f:
            for row in row_list:
                line = ','.join(row)
                print(f"[{datetime.datetime.now()}]  [rewrite]  {line}")
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

    data_table = []

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[read line]  {line}")

        # ［投票区の番号］、［施設名］、［住所］か判断
        #
        #   例： `第１ 野辺地区会館 野辺１２６番地４`
        #
        #
        # ただし、どうしようもないやつもある。こういうのは手作業で調整する
        #
        #   例： `第１１ 二宮３５０番地`
        #   例： `第１３
        #           増戸小学校屋内運動
        #           場
        #           伊奈１１７３番地`
        #
        m = re.match(r'^第([０１２３４５６７８９]+) (.*) (.*)$', line)
        if m:
            # 全角数字
            ward_number = m.group(1)

            # 半角数字に変換する。よく分かってない
            #
            #   📖 [Pythonで全角・半角を変換（mojimojiなど）](https://note.nkmk.me/python-str-convert-full-half-width/)
            #
            ward_number = int(unicodedata.normalize('NFKC', ward_number))

            name_of_facility = m.group(2)
            address = f'東京都あきる野市{m.group(3)}'
            #print(f"[ward   ] {ward_number}  施設名:{name_of_facility}")

            # データ・テーブル
            data_table.append([ward_number, address, name_of_facility])
            continue


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        # ヘッダー
        f.write(f'{to_formatted_header_string()}\n')

        for data_record in data_table:
            ward_number = data_record[0]
            name_of_facility = data_record[1]
            address = data_record[2]

            # 出力フォーマット
            output_line = to_formatted_data_record_string(
                    ward_number=ward_number,
                    address=address,
                    name_of_facility=name_of_facility)
            #print(output_line)
            f.write(f'{output_line}\n')


    #
    # 以下、データ内容に加工が必要なものは、調整します
    #
    processing_data()

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
