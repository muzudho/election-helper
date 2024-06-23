#
# cd 2024_tokyo
# python voting_station_1.py
#
import re

########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # 実施期間 実施時間
    #
    #   例： 4/17 ～ 4/22 8:30 ～ 20:00
    #
    ptn_time = r'\d+/\d+ ～ \d+/\d+ \d+:\d+ ～ \d+:\d+'

    # 改行されて月日だけのケース
    #
    #   例： 4/22
    #
    ptn_time2 = r'\d+/\d+'

    # 実施期間 実施時間　表記揺れ
    #
    #   例： 4/18 ～ 4/21 10:00 20:00
    #
    ptn_time3 = r'\d+/\d+ ～ \d+/\d+ \d+:\d+ \d+:\d+'

    # ファイル読取
    with open('voting_station_1_input_data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:

        if line.startswith('令和5年') or line.startswith('区市町村名') or line.startswith('施設名') or line.startswith('計 ') or line.startswith('※'):
            print(f"[ignored] {line}", end='')
            continue

        # 前後の空白、改行を除去
        line = line.strip()

        print(f"[read   ] {line}")

        # 実施期間 実施時間は削除
        line = re.sub(ptn_time, '', line)
        line = re.sub(ptn_time2, '', line)
        line = re.sub(ptn_time3, '', line)

        print(f"[       ] {line}")

