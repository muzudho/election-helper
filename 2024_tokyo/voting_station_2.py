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
    # ページのヘッダー
    '本文へスキップします。',
    '東京都選挙管理委員会',
    '文字サイズ・色合い変更',
    '都庁総合ホームページ',
    'トップ',
    '立候補者一覧',
    '選挙公報',
    '期日前投票所一覧',
    '都議会議員補欠選挙',
    '投開票速報',
    '期日前投票所一覧',
    'トップページ',
    '期日前投票所一覧',
    '※',
    '区市町村をお選びください',

    # テーブルのヘッダー
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


########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    with open('voting_station_2_input_data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()


    # 見出し
    town_name = None

    #succeed_table = []
    #failed_table = []

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
            address = m.group(2).strip()

            print(f'''"{town_name}", "{building}", "{address}"''')
            #succeed_table.append(f'''"{town_name}", "{building}", "{address}"''')

        else:
            print(f'''[parse error] "{town_name}", "{line}"''')
            #failed_table.append(f'''[parse error] "{town_name}", "{line}"''')


    #for succeed_line in succeed_table:
    #    print(succeed_line)


    #for failed_line in failed_table:
    #    print(failed_line)