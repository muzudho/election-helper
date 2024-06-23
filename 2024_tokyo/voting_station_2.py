#
# cd 2024_tokyo
# python voting_station_2.py
#
import re


########################################
# 準備
########################################

# 除外行の行頭の語句
starts_of_ignore_row = [
    '施設名',

    # ページのフッター
    'ページの先頭へ戻る',
    'サイトマップ',
    'お問い合せ・連絡先',
    '関係機関リンク集',
    'サイトポリシー',
    'アクセシビリティ方針',
    '個人情報保護方針',
    'お問い合わせ',
    '東京都庁：〒',
    'Copyright (C)',
]


def is_ignore_line(line):
    """この行を無視するか？"""

    # 空行
    if line == '':
        return True

    shall_ignore = False

    for word in starts_of_ignore_row:
        if line.startswith(word):
            #print(f"[ignored] {line}  word:`{word}`")
            shall_ignore = True
            break

    return shall_ignore


# 実施期間 実施時間
#
#   例： 4/17 ～ 4/22 8:30 ～ 20:00
#
ptn_time = r'\d+/\d+\s*～\s*\d+/\d+\s+\d+:\d+\s*～\s*\d+:\d+'

# 改行されて月日だけのケース
#
#   例： 4/22
#
ptn_time2 = r'\d+/\d+'

# 実施期間 実施時間　表記揺れ
#
#   例： 4/18 ～ 4/21 10:00 20:00
#
ptn_time3 = r'\d+/\d+\s*～\s*\d+/\d+\s+\d+:\d+\s+\d+:\d+'

# 実施期間 実施時間　表記揺れ
#
#   例： 6/21～7/6       8:30～20:00
#
ptn_time4 = r'\d+/\d+～\d+/\d+\s+\d+:\d+～\d+:\d+'


def remove_time(line):
    """実施期間 実施時間 の削除"""
    line = re.sub(ptn_time, '', line)
    line = re.sub(ptn_time2, '', line)
    line = re.sub(ptn_time3, '', line)
    line = re.sub(ptn_time4, '', line)

    return line


########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    with open('voting_station_2_input_data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:

        # 前後の空白、改行を除去
        line = line.strip()

        # 除外行
        if is_ignore_line(line):
            continue

        #print(f"[read   ] {line}")

        # 実施期間 実施時間は削除
        line = remove_time(line)

        print(f"[read   ] {line}")

