#
# cd 2024_tokyo/vote_on_the_day/akiruno
# python make_csv.py
#
import re
import datetime


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

        #print(f"[read line]  {line}")

        # ［投票区の番号］、［施設名］、［住所］か判断
        #
        #   例： `第１ 野辺地区会館 野辺１２６番地４`
        #
        m = re.match(r'^第([０１２３４５６７８９]+) (.*) (.*)$', line)
        if m:
            # 全角数字
            ward_number = m.group(1)

            name_of_facility = m.group(2)
            address = f'東京都あきる野市{m.group(3)}'
            #print(f"[ward   ] {ward_number}  施設名:{name_of_facility}")

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

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
