#
# cd 2024_tokyo
# python voting_station.py
#

########################################
# スクリプト実行時
########################################

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    with open('voting_station_input_data.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        print(f"[read] {line}", end='')
