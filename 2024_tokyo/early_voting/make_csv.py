#
# cd 2024_tokyo/early_voting
# python make_csv.py
#
import re


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_early_voting.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
本文へスキップします。

東京都選挙管理委員会
文字サイズ・色合い変更
都庁総合ホームページ
サイトマップ



トップ	
立候補者一覧
選挙公報
期日前投票所一覧
都議会議員補欠選挙
投開票速報
期日前投票所一覧
トップページ さまざまな投票制度 期日前投票所一覧
期日前投票所一覧
※区市町村名の（　）内は期日前投票所数


区市町村をお選びください




施設名	所在地	実施期間	実施時間




ページの先頭へ戻る
サイトマップ
お問い合せ・連絡先
関係機関リンク集
 サイトポリシー 
アクセシビリティ方針 
個人情報保護方針 
お問い合わせ 
東京都庁：〒163-8001 東京都新宿区西新宿2-8-1 電話：03-5321-1111（代表）

Copyright (C) 2024 Tokyo Metropolitan Government. All Rights Reserved.
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


# 実施期間 実施時間
patterns_of_time = [
    # 例： 4/17 ～ 4/22 8:30 ～ 20:00
    r'\d+/\d+\s*～\s*\d+/\d+\s+\d+:\d+\s*～\s*\d+:\d+',

    # 例： 4/22   ※改行されて月日だけのケース
    r'\d+/\d+',

    # 例： 4/18 ～ 4/21 10:00 20:00
    r'\d+/\d+\s*～\s*\d+/\d+\s+\d+:\d+\s+\d+:\d+',

    # 例： 6/21～7/6       8:30～20:00
    r'\d+/\d+～\d+/\d+\s+\d+:\d+～\d+:\d+',

    # 例： 10:00～17:00
    r'\d+:\d+～\d+:\d+',
]


def remove_time(line):
    """実施期間 実施時間 の削除"""
    for pattern in patterns_of_time:
        line = re.sub(pattern, '', line)

    return line


def double_quote(text):
    """カンマが含まれていれば、二重引用符で囲む"""
    if ',' in text:
        return f'"{text}"'

    return text


########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    print(f'read `{input_file_name}` file...')

    with open(input_file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()


    # 見出し
    town_name = None

    output_table = []

    # 出力フォーマット
    #
    #   WKT を使うともっといい？
    #   `WKT` - 例えば緯度・経度。 例： `"POINT (139.4102538 35.7554727)"`
    #
    output_table.append(f'''住所, 施設名''')

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[read   ] {line}")

        # 町？名か判断
        m = re.match(r'(.+)[\(（]\d+[\)）]', line)
        if m:
            town_name = m.group(1)
            #print(f"[town   ] {town_name}")
            continue

        # 実施期間 実施時間は削除
        line = remove_time(line).strip()

        if line == '':
            continue

        # 最初に出てくるタブまでが建物名と仮定して抽出
        m = re.match(r'(.+)\t(.*)', line)
        if m:
            building = m.group(1).strip()

            # TODO 住所から［地下1階］は除去したい
            # TODO ［東京都調布市西つつじヶ丘3-19-1, つつじケ丘児童館ホール］は川の上になってしまう。［東京都調布市西つつじヶ丘 つつじケ丘児童館ホール］に変えたい
            address = f'東京都{m.group(2).strip()}'

            # 出力フォーマット
            output_table.append(f'''{double_quote(address)}, {double_quote(building)}''')

        else:
            raise ValueError(f'''[parse error] "{town_name}", "{line}"''')


    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"please read `{output_file_name}` file")
