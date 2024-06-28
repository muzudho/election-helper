#
# cd 2024_tokyo/vote_on_the_day/fuchu
# python edit_csv.py
#
import re
import csv
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data_fuchu_edit.csv'
output_file_name = 'output_data_fuchu_edit.csv'


########################################
# スクリプト実行時
########################################

# 以下みたいな感じになってるから、
#
# 投票区番号,施設名,住所,ライセンス
# 1,市立第八中学校,東京都府中市四谷1-2827,「CC-BY（表示）」府中市のデータを使用しています
# 2,四谷文化センタ－,東京都府中市四谷2-75,「CC-BY（表示）」府中市のデータを使用しています
# 3,西府文化センタ－,東京都府中市西府町1-60,「CC-BY（表示）」府中市のデータを使用しています
#
#
# 以下みたいな感じに整形する
#
# 投票区番号,住所,施設名,ライセンス
# 1,東京都府中市四谷1-2827 市立第八中学校,市立第八中学校,「CC-BY（表示）」府中市のデータを使用しています
# 2,東京都府中市四谷2-75 四谷文化センタ－,四谷文化センタ－,「CC-BY（表示）」府中市のデータを使用しています
# 3,東京都府中市西府町1-60 西府文化センタ－,西府文化センタ－,「CC-BY（表示）」府中市のデータを使用しています
#

if __name__ == '__main__':
    """スクリプト実行時"""

    # ファイル読取
    print(f'[{datetime.datetime.now()}]  read `{input_file_name}` file...')

    with open(input_file_name, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        # 二次元配列
        row_list = [row for row in reader]

        # ヘッダー
        header_row = row_list[0]
        #header_of_ward_number = header_row[0]
        header_of_name_of_facility = header_row[1]
        header_of_address = header_row[2]

        row_list[0][1] = header_of_address
        row_list[0][2] = header_of_name_of_facility

        for i in range(1, len(row_list)):
            row = row_list[i]
            #print(f'[{datetime.datetime.now()}]  [processing]  {row}')

            #ward_number = row[0]
            name_of_facility = row[1]
            address = row[2]

            row[1] = f'{address} {name_of_facility}'
            row[2] = name_of_facility


    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for row in row_list:
            output_line = ','.join(row)
            #print(output_line)
            f.write(f'{output_line}\n')

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
