#
# cd 2024_tokyo/vote_on_the_day/kiyose
# python make_csv.py
#
import re
import datetime


########################################
# 設定
########################################

input_file_name = 'input_data.txt'
output_file_name = 'output_data_kiyose.csv'


########################################
# 準備
########################################

# 除外行のリスト（テキスト入力）
except_lines_as_text = """\
エンターキーを押すと、ナビゲーション部分をスキップし本文へ移動します。
清瀬市公式ホームページトップページ
サイトマップ Language やさしい日本語 読み上げ 文字サイズ・配色の変更
緊急・防災情報
 
清瀬駅開業100周年記念
 
きよせのーと
 
50周年記念ページ
くらし・手続き
子育て
健康・医療・福祉
文化・スポーツ・観光
仕事・産業
市政情報
キーワードから探す 
 検索
現在の位置：  トップページ > 市政情報 > 選挙 > あなたのお住まいの投票所 > あなたのお住まいの投票所一覧

ここから本文です。
あなたのお住まいの投票所一覧
ページ番号1004883　 更新日 2024年6月6日印刷大きな文字で印刷




より良いウェブサイトにするために、ページのご感想をお聞かせください。
このページに問題点はありましたか？（複数回答可）
特にない 内容が分かりにくい ページを探しにくい 情報が少ない 文章量が多い
このページの情報は役に立ちましたか？
役に立った 役に立たなかった
このページは見つけやすかったですか？
見つけやすかった 見つけにくかった
送信

このページに関するお問い合わせ
選挙管理委員会事務局選挙係
〒204-8511
東京都清瀬市中里5-842　清瀬市役所2階
電話番号（直通）：042-497-2561
電話番号（代表）：042-492-5111
ファクス番号：042-492-2415
お問い合わせは専用フォームをご利用ください。

市政情報
選挙
あなたのお住まいの投票所
あなたのお住まいの投票所一覧
ページの先頭へ戻る
前のページへ戻る トップページへ戻る
表示
PC
スマートフォン
ホームページの使い方 著作権・免責事項 個人情報の取り扱い ウェブアクセシビリティ
注目情報

清瀬駅開業
100周年記念

清瀬市
50周年記念

魅力発信！
きよせのーと。

イベントカレンダー
清瀬市役所
〒204-8511　東京都清瀬市中里5丁目842番地（交通アクセス）
※この郵便番号は、清瀬市役所の個別郵便番号です。
電話番号：042-492-5111（代表）
開庁時間：月曜日から金曜日の午前8時30分から午後5時まで

清瀬市は、東京都の多摩地域北東部に位置しています。
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

        #print(f"[read   ] {line}")

        # 投票区の番号か判断
        #
        #   例： `投票区　1`
        #
        m = re.match(r'投票区　(\d+)', line)
        if m:

            # 前のを flush
            if ward_number != None:
                # 出力フォーマット
                output_table.append(to_formatted_data_record_string(
                        ward_number=ward_number,
                        address=address,
                        name_of_facility=name_of_facility))


            ward_number = m.group(1)
            #print(f"[ward num] {ward_number}")
            continue

        # 投票所（施設名）か判断
        #
        #   例： `投票所第1投票所投票所建物名称及び所在地市立清明小学校`
        #
        m = re.match(r'投票所第\d+投票所投票所建物名称及び所在地(.*)', line)
        if m:
            name_of_facility = m.group(1)
            #print(f"[name of facility] {name_of_facility}")
            continue

        # 住所か判断
        #
        #   例： `清瀬市旭が丘二丁目8番1号投票区の区域旭が丘二丁目から六丁目全域`
        #
        m = re.match(r'(.*)投票区の区域.*', line)
        if m:
            address = f'東京都{m.group(1)}'
            #print(f"[address] {address}")
            continue


    # 前のを flush
    if ward_number != None:
        # 出力フォーマット
        output_table.append(to_formatted_data_record_string(
                ward_number=ward_number,
                address=address,
                name_of_facility=name_of_facility))


    print(f"[{datetime.datetime.now()}]  write `{output_file_name}` file...")

    # ファイル書出し
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in output_table:
            #print(line)
            f.write(f'{line}\n')

    print(f"[{datetime.datetime.now()}]  please read `{output_file_name}` file")
